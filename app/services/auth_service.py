from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.models.user import UserModel
from app.core.security import hash_password, verify_password
from app.core.exceptions import bad_request


def register_user(user_data: UserCreate, db: Session):
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()

    if (existing_user):
        raise bad_request("Email đã được sử dụng")

    hashed_password = hash_password(user_data.password)

    allowed_roles = ["USER", "ADMIN"]
    role = user_data.role.upper()

    if (role not in allowed_roles):
        raise bad_request("Role không hợp lệ")

    new_user = UserModel(
        email = user_data.email,
        password_hash = hashed_password,
        fullname = user_data.fullname,
        role = role,
        is_active = user_data.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(user_data: UserLogin, db: Session):

    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()

    if (not user or not verify_password(user_data.password, user.password_hash)):
        raise bad_request("Email hoặc Mặt khẩu không đúng")

    return user