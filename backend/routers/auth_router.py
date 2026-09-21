from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import User
from backend.db.schemas import RegisterUserCreate, RegisterUserResponse, TokenResponse
from backend.auth.utils import hash_password, verify_password
from backend.auth.jwt import create_access_token, oauth2_scheme, token_blocklist
from backend.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.post("/register", response_model=RegisterUserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, user_data: RegisterUserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hardcode role to 'user' to prevent privilege escalation
    new_user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(token: str = Depends(oauth2_scheme)):
    if token in token_blocklist:
        raise HTTPException(status_code=401, detail="Token already invalidated")

    token_blocklist.add(token)
    return {"message": "Successfully logged out"}