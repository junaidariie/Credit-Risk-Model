import os
import uuid
import shutil
import tempfile
import edge_tts

from fastapi import FastAPI, HTTPException, UploadFile, File, Query, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from inference.predictor import CreditRiskPredictor
from advisor_bot import generate_advice_stream
from chatbot_advisor import ask_chatbot_stream
from faster_whisper.tokenizer import _LANGUAGE_CODES
from whisper_service import model
from backend.limiter import limiter
# DB and Authentication Dependencies
from backend.db.database import get_db, SessionLocal, engine, Base
from backend.db.models import User, PredictionLog
from backend.db.schemas import CreditRiskInput, CreditRiskOutput, ChatMessage, TTS_REQUEST
from backend.auth.jwt import get_current_user
from backend.auth.utils import hash_password

# Routers
from backend.routers import auth_router, user_router, admin_router

# ================== APP INIT ================== #
app = FastAPI(title="RiskGuard AI - Credit Risk Engine")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

# Include Modular Routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(admin_router.router)

# Subtitle Cache
subtitle_cache = {}

# Predictor Engine
predictor = CreditRiskPredictor()


# ================== STARTUP HOOK (AUTO ADMIN CREATION) ================== #
@app.on_event("startup")
def startup_init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if an admin account exists
        admin_user = db.query(User).filter(User.role == "admin").first()
        if not admin_user:
            admin_username = os.getenv("ADMIN_USERNAME", "admin")
            admin_password = os.getenv("ADMIN_PASSWORD", "AdminPass123!")

            new_admin = User(
                username=admin_username,
                password_hash=hash_password(admin_password),
                role="admin",
                is_active=True
            )
            db.add(new_admin)
            db.commit()
            print(f"[INIT] Created default admin account: '{admin_username}'")
    finally:
        db.close()


# ================== HEALTH ================== #
@app.get("/")
def root():
    return {"status": "RiskGuard AI API is running."}


# ================== STREAMING ADVISOR RESPONSE ================== #
@app.post("/predict_credit_risk_stream", response_model=CreditRiskOutput)
@limiter.limit("20/minute")
async def predict_credit_risk_stream(
        request: Request,
        input_data: CreditRiskInput,
        current_user: User = Depends(get_current_user),
):
    try:
        input_dict = input_data.dict()
        probability, credit_score, rating = predictor.predict(input_dict)

        async def event_generator():
            yield f"probability:{probability}\n"
            yield f"credit_score:{credit_score}\n"
            yield f"rating:{rating}\n"

            advisor_chunks = []
            for chunk in generate_advice_stream(
                    probability=probability,
                    credit_score=credit_score,
                    rating=rating,
            ):
                advisor_chunks.append(chunk)
                yield f"advisor:{chunk}\n"

            # Single DB write after streaming completes
            prediction_record = PredictionLog(
                user_id=current_user.user_id,
                **input_dict,
                probability=probability,
                credit_score=credit_score,
                rating=rating,
                advisor_response="".join(advisor_chunks)
            )
            save_db = SessionLocal()
            try:
                save_db.add(prediction_record)
                save_db.commit()
            finally:
                save_db.close()

        return StreamingResponse(event_generator(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================== CHAT STREAM ================== #
@app.post("/chat")
@limiter.limit("30/minute")
async def chat(
        request: Request,
        message_data: ChatMessage,
        current_user: User = Depends(get_current_user)
):
    async def event_generator():
        for chunk in ask_chatbot_stream(
                message_data.probability,
                message_data.credit_score,
                message_data.rating,
                message_data.advisor_reply,
                message_data.message,
                message_data.thread_id
        ):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")


# ================== TTS ================== #
async def audio_generator(request_id, text, voice, volume, rate):
    try:
        communicate = edge_tts.Communicate(text=text, voice=voice, volume=volume, rate=rate)
        submaker = edge_tts.SubMaker()
        async for chunk in communicate.stream():
            if chunk["type"] == 'audio':
                yield chunk['data']
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

        subtitle_cache[request_id] = submaker.get_srt()
    except Exception:
        raise HTTPException(status_code=500, detail="error generating audio")


@app.post("/tts")
async def tts(tts_params: TTS_REQUEST, current_user: User = Depends(get_current_user)):
    try:
        request_id = str(uuid.uuid4())
        return StreamingResponse(
            audio_generator(
                text=tts_params.text,
                voice=tts_params.voice,
                volume=tts_params.volume,
                rate=tts_params.rate,
                request_id=request_id
            ),
            media_type='audio/mpeg',
            headers={"X-Request-ID": request_id},
        )
    except Exception:
        raise HTTPException(status_code=500, detail="error generating audio")


@app.get("/subtitles/{request_id}")
async def get_subtitles(request_id: str):
    srt = subtitle_cache.pop(request_id, None)
    if srt is None:
        raise HTTPException(status_code=404, detail="Subtitles not ready")
    return {'request_id': request_id, 'subtitles': srt}


@app.get('/tts_available_voices')
async def available_voices():
    try:
        voices = await edge_tts.list_voices()
        simplified = [{"Voice": v['ShortName'], "Gender": v['Gender']} for v in voices]
        return {"Available Voices": len(voices), "Voices": simplified}
    except Exception:
        raise HTTPException(status_code=500, detail='error fetching available voices')


# ================== STT ================== #
@app.get('/stt_supported_voices')
async def stt_supported_voices():
    try:
        supported_languages = sorted(_LANGUAGE_CODES)
        return {"Total Languages": len(_LANGUAGE_CODES), "Supported Languages": supported_languages}
    except Exception:
        raise HTTPException(status_code=500, detail='error fetching supported languages')


def transcribe_audio(file_path: str, translation: bool = False, language_detection: bool = False):
    try:
        task_type = "translate" if translation else "transcribe"
        segments, info = model.transcribe(file_path, task=task_type, beam_size=3, vad_filter=True)
        result = {"segments": [segment.text for segment in segments]}
        if language_detection:
            result["detected_language"] = info.language
            result["language_probability"] = info.language_probability
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error transcribing audio: {str(e)}")


@app.post("/stt")
async def stt(
        file_path: UploadFile = File(...),
        translation: bool = Query(False),
        language_detection: bool = Query(False),
        current_user: User = Depends(get_current_user)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            shutil.copyfileobj(file_path.file, temp)
            temp_path = temp.name

        result = transcribe_audio(file_path=temp_path, translation=translation, language_detection=language_detection)
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="error generating captions")