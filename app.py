from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prediction_helper import predict
from advisor_bot import generate_advice

app = FastAPI()

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

@app.get("/")
def greeting():
    return {"message":"Hello world!!"}

@app.get("/home")
def hello():
    return {"message":"Hey, The Server for credit risk prediction is ALIVE!"}

@app.post("/predict_credit_risk", response_model=CreditRiskOutput)
def predict_credit_risk(input_data: CreditRiskInput):
    print("Request received")
    try:
        probability, credit_score, rating = predict(input_data.age, input_data.income, input_data.loan_amount,
                                                    input_data.loan_tenure_months, input_data.avg_dpd_per_delinquency,
                                                    input_data.delinquency_ratio, input_data.credit_utilization_ratio,
                                                    input_data.num_open_accounts, input_data.residence_type,
                                                    input_data.loan_purpose, input_data.loan_type)
        
        advisor_reply = generate_advice(probability=probability, credit_score=credit_score, rating=rating)
        return CreditRiskOutput(probability=probability, credit_score=credit_score, rating=rating, advisor_response=advisor_reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
