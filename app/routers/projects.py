from fastapi import APIRouter, Depends, status
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate, ProjecDetailtResponse
from app.schemas.project_members import ProjectMemberResponse, ProjectMemberDetailResponse
from app.db.database import get_db
import app.services.project_service as service
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.dependencies.dependencie import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate, 
    current_data: UserModel = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return service.create_project_service(project_data, current_data, db)

@router.get("", response_model=list[ProjectResponse])
def get_project(
    name: str | None = None,
    current_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service.get_project_service(db, current_data, name)

@router.get("/{id}", response_model=ProjecDetailtResponse)
def get_project_by_id(
    id: int, 
    current_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service.get_project_by_id_service(db, current_data, id)

@router.put("/{id}", response_model=ProjectResponse)
def update_project(
    id: int,
    data: ProjectUpdate,
    current_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service.update_project_service(db, current_data, id, data)

@router.delete("/{id}")
def delete_project(
    id: int, 
    current_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service.delete_project_service(db, current_data, id)

