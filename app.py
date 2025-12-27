from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import os

from prediction_helper import predict
from advisor_bot import generate_advice
from chatbot_advisor import ask_chatbot
from utility import STT, TTS

app = FastAPI()

# ---------------- CORS ---------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODELS ---------------- #

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


class TTSRequest(BaseModel):
    text: str


# ---------------- BASIC ROUTES ---------------- #

@app.get("/")
def root():
    return {"message": "Hello world!!"}


@app.get("/home")
def home():
    return {"message": "Credit Risk API is running."}


# ---------------- CREDIT RISK ---------------- #

@app.post("/predict_credit_risk", response_model=CreditRiskOutput)
def predict_credit_risk(input_data: CreditRiskInput):
    try:
        probability, credit_score, rating = predict(
            input_data.age,
            input_data.income,
            input_data.loan_amount,
            input_data.loan_tenure_months,
            input_data.avg_dpd_per_delinquency,
            input_data.delinquency_ratio,
            input_data.credit_utilization_ratio,
            input_data.num_open_accounts,
            input_data.residence_type,
            input_data.loan_purpose,
            input_data.loan_type
        )

        advisor_reply = generate_advice(
            probability=probability,
            credit_score=credit_score,
            rating=rating
        )

        return CreditRiskOutput(
            probability=probability,
            credit_score=credit_score,
            rating=rating,
            advisor_response=advisor_reply
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- CHAT STREAM ---------------- #

@app.post("/chat")
async def chat(message_data: ChatMessage):

    async def event_generator():
        for chunk in ask_chatbot(
            message_data.probability,
            message_data.credit_score,
            message_data.rating,
            message_data.advisor_reply,
            message_data.message,
            message_data.thread_id
        ):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")


# ---------------- TTS ---------------- #

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text is empty")

        audio_path = await TTS(text=request.text)

        if not os.path.exists(audio_path):
            raise HTTPException(status_code=500, detail="Audio file not created")

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename="speech.mp3"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- STT ---------------- #

@app.post("/stt")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        return await STT(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

