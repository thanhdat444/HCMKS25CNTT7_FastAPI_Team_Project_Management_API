from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse, UserCreate
from sqlalchemy.orm import Session
from app.db.database import get_db
import app.services.auth_service as service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model = UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return service.register_user(user_data, db)