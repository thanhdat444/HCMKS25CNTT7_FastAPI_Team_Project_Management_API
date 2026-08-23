from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse, UserCreate, UserLogin
from sqlalchemy.orm import Session
from app.db.database import get_db
import app.services.auth_service as service_auth
from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model = UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return service_auth.register_user(user_data, db)

@router.post("/login")
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = service_auth.authenticate_user(user_data, db)

    access_token = create_access_token(
        data={
            "sub": user.email,
            "id": user.id,
            "role": user.role
        }
    )

    return {
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "email": user.email,
            "fullname": user.fullname,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    }