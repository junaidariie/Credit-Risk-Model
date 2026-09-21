from pydantic import BaseModel, ConfigDict, Field

# ==========================================
# AUTH SCHEMAS
# ==========================================

class RegisterUserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="Username (3-20 chars)")
    password: str = Field(..., min_length=8, max_length=64, description="Password (min 8 chars)")


class RegisterUserResponse(BaseModel):
    user_id: int
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class LoginUser(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ==========================================
# PREDICTION SCHEMAS
# ==========================================

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
    text: str
    voice: str = "en-GB-SoniaNeural"
    rate: str = "+0%"
    volume: str = "+0%"