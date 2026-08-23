from fastapi import APIRouter, Depends
from app.models.user import UserModel
from app.dependencies.dependencie import get_current_user

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