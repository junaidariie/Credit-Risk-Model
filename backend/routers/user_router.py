from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.jwt import get_current_user
from backend.db.database import get_db
from backend.db.models import User, PredictionLog
from backend.db.schemas import RegisterUserResponse

router = APIRouter(prefix="/user", tags=["User Actions"])

@router.get("/me", response_model=RegisterUserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Fetch profile details for the authenticated user."""
    return current_user

@router.get("/my-history")
def get_my_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch past credit predictions made by the logged-in user."""
    history = db.query(PredictionLog).filter(PredictionLog.user_id == current_user.user_id).all()
    return history