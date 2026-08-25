from app.models.task import TaskModel
from app.models.project_members import ProjectMemberModel
from app.models.user import UserModel
from app.schemas.task import TaskCreate
from sqlalchemy.orm import Session
from app.core.exceptions import forbidden, not_found
from app.models.task import TaskModel


def create_task_service(
    db: Session,
    current_user: UserModel,
    project_id: int,
    task_data: TaskCreate
):
    member = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.user_id == current_user.id,
            ProjectMemberModel.project_id == project_id
        )
        .first()
    )

    if (not member):
        raise forbidden("You are not a member of this project")

    new_task = TaskModel(
        project_id=project_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def get_tasks_service(
    db: Session,
    current_user: UserModel,
    project_id: int,
):
    member = (
        db.query(ProjectMemberModel)
        .filter(
            current_user.id == ProjectMemberModel.user_id,
            project_id == ProjectMemberModel.project_id
        )
        .first()
    )

    if (not member):
        raise forbidden("You are not a member of this project")

    tasks = (
        db.query(TaskModel)
        .filter(
            project_id == TaskModel.project_id
        )
        .all()
    )

    return tasks

def get_task_by_id_service(
    db: Session,
    task_id: int,
    current_data: UserModel
):
    task = (
        db.query(TaskModel)
        .filter(
            TaskModel.id == task_id
        )
        .first()
    )

    if (not task):
        raise not_found("Task not found")

    member = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.user_id == current_data.id,
            ProjectMemberModel.project_id == task.project_id
        )
        .first()
    )

    if not member:
        raise forbidden("You are not a member of this project")

    return task