from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.jwt import require_role
from backend.db.database import get_db
from backend.db.models import User, PredictionLog
from backend.db.schemas import RegisterUserResponse

router = APIRouter(prefix="/admin", tags=["Admin Actions"])

# Restrict all routes in this file to users with 'admin' role
admin_guard = Depends(require_role(["admin"]))

@router.get("/stats", dependencies=[admin_guard])
def get_system_stats(db: Session = Depends(get_db)):
    """Get high-level system usage statistics."""
    return {
        "total_users": db.query(User).count(),
        "total_predictions": db.query(PredictionLog).count()
    }

@router.get("/users", response_model=list[RegisterUserResponse], dependencies=[admin_guard])
def get_all_users(db: Session = Depends(get_db)):
    """List all registered users."""
    return db.query(User).all()

@router.get("/predictions", dependencies=[admin_guard])
def get_all_predictions(db: Session = Depends(get_db)):
    """List all credit predictions across all users."""
    return db.query(PredictionLog).all()

@router.get("/user/{user_id}/predictions", dependencies=[admin_guard])
def get_user_predictions(user_id: int, db: Session = Depends(get_db)):
    """Get full input/output prediction records for a specific user."""
    return db.query(PredictionLog).filter(PredictionLog.user_id == user_id).all()

@router.put("/promote/{user_id}", dependencies=[admin_guard])
def promote_user_to_admin(user_id: int, db: Session = Depends(get_db)):
    """Promote a standard user account to admin role."""
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = "admin"
    db.commit()
    return {"message": f"User '{user.username}' promoted to admin successfully."}