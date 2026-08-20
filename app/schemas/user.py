from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    fullname: str
    role: str = "USER"
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: EmailStr | None = None
    fullname: str | None = None
    role: str | None = None
    is_active: bool | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)