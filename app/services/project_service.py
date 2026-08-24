from app.schemas.project import ProjectCreate
from sqlalchemy import or_
from app.models.project import ProjectModel
from app.models.project_members import ProjectMemberModel
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.core.exceptions import not_found

def create_project_service(
    project_data: ProjectCreate, 
    current_data: UserModel, 
    db: Session
):
    new_project = ProjectModel(
        name = project_data.name,
        description = project_data.description,
        owner_id = current_data.id
    )

    db.add(new_project)
    db.flush()

    owner_member = ProjectMemberModel(
        project_id = new_project.id,
        user_id = current_data.id,
        role = "OWNER"
    )

    db.add(owner_member)
    db.commit()

    db.refresh(new_project)

    return new_project

def get_project_service(db: Session, current_data: UserModel, name: str | None = None):
    query = (
        db.query(ProjectModel)
        .outerjoin(
            ProjectMemberModel, 
            ProjectMemberModel.project_id == ProjectModel.id
        )
        .filter(
            or_(
                ProjectModel.owner_id == current_data.id,
                ProjectMemberModel.user_id == current_data.id
            )
        )
    )

    if (name):
        query = query.filter(ProjectModel.name.ilike(f"%{name}%"))

    return query.distinct().all()

def get_project_by_id_service(
    db: Session, 
    current_data: UserModel, 
    project_id : int
):
    project = (
        db.query(ProjectModel)
        .outerjoin(
            ProjectMemberModel, 
            ProjectMemberModel.project_id == ProjectModel.id
        )
        .filter(
            ProjectModel.id == project_id,
            ProjectMemberModel.user_id == current_data.id
        )
        .first()
    )

    if not project:
        raise not_found("Project not found or you are not a member of this project")

    return project