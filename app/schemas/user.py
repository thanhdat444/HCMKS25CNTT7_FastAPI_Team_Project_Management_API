from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    fullname: str = Field(min_length=2, max_length=255)
    role: str = "USER"
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=255)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=255)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    fullname: str | None = Field(default=None, min_length=2, max_length=255)
    role: str | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=6, max_length=255)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)