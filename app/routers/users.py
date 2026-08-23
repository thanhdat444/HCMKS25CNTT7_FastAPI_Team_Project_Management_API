from fastapi import APIRouter, Depends
from app.models.user import UserModel
from app.dependencies.dependencie import get_current_user, RoleChecker
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def get_my_profile(current_user: UserModel = Depends(get_current_user)):
    return {
        "message": "Xác thực thành công!",
        "user_info": {
            "id": current_user.id,
            "email": current_user.email,
            "fullname": current_user.fullname,
            "role": current_user.role
        }
    }

@router.get("", response_model=list[UserResponse])
def get_users(
    name: str | None = None,
    email: str | None = None,
    is_active: bool | None = None,

    current_user: UserModel = Depends(
        RoleChecker(["ADMIN"])
    ),

    db: Session = Depends(get_db)
):
    query = db.query(UserModel)

    if name:query = query.filter(UserModel.fullname.contains(name))

    if email:
        query = query.filter(UserModel.email.contains(email))

    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)

    return query.all()