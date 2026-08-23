from fastapi import APIRouter, Depends
from app.models.user import UserModel
from app.dependencies.dependencie import get_current_user, RoleChecker

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

@router.get("")
def get_admin_dashboard(current_user: UserModel = Depends(RoleChecker(["ADMIN"]))):
    return {
        "status": "success",
        "message": "Chào mừng Admin!",
        "secret_data": "Đây là dữ liệu tuyệt mật chỉ Admin mới thấy."
    }