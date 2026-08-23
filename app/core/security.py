import bcrypt
import jwt
from app.core.config import settings
from datetime import datetime, timezone, timedelta

def hash_password(password: str, cost_factor: int = 12) -> str:
    password_byte = password.encode("utf-8")
    salf = bcrypt.gensalt(rounds=cost_factor)
    hashed_password = bcrypt.hashpw(password_byte, salf)

    return hashed_password.decode("utf-8")

def verify_password(user_password: str, hashed_password: str) -> bool:
    password_byte = user_password.encode("utf-8")
    hashed_byte = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_byte, hashed_byte)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)