from app.models.task import TaskModel
from app.models.project_members import ProjectMemberModel
from app.models.user import UserModel
from app.schemas.task import TaskCreate, TaskUpdate
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
    status: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    title: str | None = None
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

    query = (
        db.query(TaskModel)
        .filter(project_id == TaskModel.project_id)
    )

    if (status):
        query = query.filter(TaskModel.status == status)

    if priority:
        query = query.filter(TaskModel.priority == priority)

    if assignee_id:
        query = query.filter(TaskModel.assignee_id == assignee_id)

    if title:
        query = query.filter(TaskModel.title.ilike(f"%{title}%"))

    return query.all()

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

def update_task_service(
    task_id: int,
    task_data: TaskUpdate,
    current_data: UserModel,
    db: Session
):
    task = (
        db.query(TaskModel)
        .filter(
            task_id == TaskModel.id
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

    if (not member):
        raise forbidden("You are not a member of this project")

    update_data = task_data.model_dump(exclude_unset=True)

    user = (
        db.query(UserModel)
        .filter(UserModel.id == task_data.assignee_id)
        .first()
    )

    if (not user):
        raise not_found("Assignee not found")

    if "assignee_id" in update_data:
        assignee_member = (
            db.query(ProjectMemberModel)
            .filter(
                ProjectMemberModel.user_id == update_data["assignee_id"],
                ProjectMemberModel.project_id == task.project_id
            )
            .first()
        )

        if (not assignee_member):
            raise forbidden("Assignee must be a member of this project")

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

def delete_task_service(
    task_id: int,
    current_data: UserModel,
    db: Session      
):
    task = (
        db.query(TaskModel)
        .filter(
            task_id == TaskModel.id
        )
        .first()
    )

    if not task:
        raise not_found("Task not found")

    member = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.user_id == current_data.id,
            ProjectMemberModel.project_id == task.project_id
        )
        .first()
    )
    
    if (not member):
        raise forbidden("You are not a member of this project")

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }