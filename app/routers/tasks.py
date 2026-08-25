from fastapi import APIRouter, Depends, status
import app.services.task_service as service
from app.schemas.task import TaskResponse, TaskCreate
from app.models.task import TaskModel
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.dependencies.dependencie import get_current_user

router = APIRouter(
    tags=["Task"]
)

@router.post("/projects/{id}/tasks", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate, 
    id: int, 
    current_user: UserModel = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return service.create_task_service(db, current_user, id, task_data)

@router.get("/projects/{id}/tasks", response_model=list[TaskResponse])
def get_tasks(
    id: int, 
    current_user: UserModel = Depends(get_current_user), 
    db: Session = Depends(get_db)
): 
    return service.get_tasks_service(db, current_user, id)

@router.get("/tasks/{id}", response_model=TaskResponse)
def get_task_by_id(
    id: int,
    current_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service.get_task_by_id_service(db, id, current_data)