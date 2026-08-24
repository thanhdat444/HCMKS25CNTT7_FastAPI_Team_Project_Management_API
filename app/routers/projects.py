from fastapi import APIRouter, Depends, status
from app.schemas.project import ProjectCreate, ProjectResponse
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