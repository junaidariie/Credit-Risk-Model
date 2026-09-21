import datetime
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.database import Base, engine


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    is_active = Column(Boolean, default=True)

    # Relationship to user predictions
    predictions = relationship("PredictionLog", back_populates="user")


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False, index=True)

    # Input Features
    age = Column(Integer, nullable=False)
    income = Column(Float, nullable=False)
    loan_amount = Column(Float, nullable=False)
    loan_tenure_months = Column(Integer, nullable=False)
    avg_dpd_per_delinquency = Column(Float, nullable=False)
    delinquency_ratio = Column(Float, nullable=False)
    credit_utilization_ratio = Column(Float, nullable=False)
    num_open_accounts = Column(Integer, nullable=False)
    residence_type = Column(String(50), nullable=False)
    loan_purpose = Column(String(100), nullable=False)
    loan_type = Column(String(50), nullable=False)

    # ML Model Outputs
    probability = Column(Float, nullable=False)
    credit_score = Column(Integer, nullable=False)
    rating = Column(String(20), nullable=False)
    advisor_response = Column(Text, nullable=True)

    # Relationship back to user
    user = relationship("User", back_populates="predictions")


Base.metadata.create_all(bind=engine)