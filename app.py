from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from inference.predictor import CreditRiskPredictor
from advisor_bot import generate_advice, generate_advice_stream
from chatbot_advisor import ask_chatbot, ask_chatbot_stream
from faster_whisper.tokenizer import _LANGUAGE_CODES
from whisper_service import model
import os
import edge_tts
import uuid
import shutil, tempfile


# ================== APP INIT ================== #

app = FastAPI(title="RiskGuard AI - Credit Risk Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

# Temporary in-memory cache
subtitle_cache = {}

# ================== LOAD MODEL ON START ================== #

predictor = CreditRiskPredictor()

# ================== SCHEMAS ================== #

class CreditRiskInput(BaseModel):
    age: int
    income: float
    loan_amount: float
    loan_tenure_months: int
    avg_dpd_per_delinquency: float
    delinquency_ratio: float
    credit_utilization_ratio: float
    num_open_accounts: int
    residence_type: str
    loan_purpose: str
    loan_type: str


class CreditRiskOutput(BaseModel):
    probability: float
    credit_score: int
    rating: str
    advisor_response: str | None = None


class ChatMessage(BaseModel):
    thread_id: str
    message: str
    probability: float
    credit_score: int
    rating: str
    advisor_reply: str


class TTS_REQUEST(BaseModel):
    text : str
    voice : str = "en-GB-SoniaNeural"
    rate : str = "+0%"
    volume : str = "+0%"


# ================== HEALTH ================== #

@app.get("/")
def root():
    return {"status": "RiskGuard AI API is running."}



# ================== STREAMING ADVISOR RESPONSE ================== #

@app.post("/predict_credit_risk_stream")
async def predict_credit_risk_stream(input_data: CreditRiskInput):
    try:
        input_dict = input_data.dict()
        probability, credit_score, rating = predictor.predict(input_dict)

        async def event_generator():
            yield f"probability:{probability}\n"
            yield f"credit_score:{credit_score}\n"
            yield f"rating:{rating}\n"

            for chunk in generate_advice_stream(
                probability=probability,
                credit_score=credit_score,
                rating=rating,
            ):
                yield f"advisor:{chunk}\n"

        return StreamingResponse(event_generator(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================== CHAT STREAM ================== #

@app.post("/chat")
async def chat(message_data: ChatMessage):

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
    except Exception as e:
        raise HTTPException(status_code=500, detail="error generating audio")


@app.post("/tts")
async def tts(tts_params : TTS_REQUEST):
    try:

        request_id = str(uuid.uuid4())

        return StreamingResponse(
            audio_generator(text=tts_params.text,
                                    voice=tts_params.voice,
                                    volume=tts_params.volume,
                                    rate=tts_params.rate,
                                    request_id=request_id
                                    ),

        media_type='audio/mpeg',
        headers={"X-Request-ID": request_id},)
    except Exception as e:
        raise HTTPException(status_code=500, detail="error generating audio")


@app.get("/subtitles/{request_id}")
async def get_subtitles(request_id : str):
    try:
        srt = subtitle_cache.pop(request_id, None)

        if srt is None:
            raise HTTPException(status_code=404, detail="Subtitles not ready")

        return {
            'request_id' : request_id,
            'subtitles' : srt
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail='error generating subtitles')
    

@app.get('/tts_available_voices')
async def available_voices():
    try:
        voices = await edge_tts.list_voices()
        simplified = [{"Voice":v['ShortName'], "Gender" : v['Gender']} for v in voices]
        num_voices = len(voices)
        return {"Available Voices" : num_voices,
                "Voices" : simplified}
    except Exception as e:
        raise HTTPException(status_code=500, detail='error fetching available voices')


# ================== STT ================== #


@app.get('/stt_supported_voices')
async def stt_supported_voices():
    try:
        supported_languages = sorted(_LANGUAGE_CODES)
        total_languages = len(_LANGUAGE_CODES)
        return {
            "TOtal Languages" : total_languages,
            "Supported Languages": supported_languages
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail='error fetching supported languages')


def transcribe_audio(file_path: str, translation: bool = False, language_detection: bool = False):
    try:
        task_type = "translate" if translation else "transcribe"
        segments, info = model.transcribe(file_path, task=task_type, beam_size=3, vad_filter=True)

        result = {
            "segments": [segment.text for segment in segments]
        }

        if language_detection:
            result["detected_language"] = info.language
            result["language_probability"] = info.language_probability

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error transcribing audio: {str(e)}")



@app.post("/stt")
async def stt(file_path : UploadFile = File(...), translation : bool = Query(False), language_detection : bool = Query(False)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            shutil.copyfileobj(file_path.file, temp)
            temp_path = temp.name

        result = transcribe_audio(file_path=temp_path, translation=translation, language_detection=language_detection)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail="error generating captions")