from app.schemas.project_members import ProjectMemberResponse, ProjectMemberDetailResponse
from fastapi import APIRouter, Depends
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.dependencie import get_current_user
import app.services.project_member_service as service

router = APIRouter(
    prefix="/projects",
    tags=["Project-Member"]
)

@router.post("/{id}/members", response_model=ProjectMemberDetailResponse)
def add_member_project(
    id: int,
    user_id: int,
    current_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service.add_member_project_service(db, current_data, id, user_id)

@router.delete("/{id}/members/{user_id}")
def delete_member_project(
    id: int,
    user_id: int,
    current_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service.delete_member_project_service(db, current_data, id, user_id)

@router.get("/{id}/members", response_model=list[ProjectMemberResponse])
def get_member_project(
    id: int,
    current_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service.get_member_project_service(id, current_data, db)