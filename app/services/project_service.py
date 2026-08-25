from app.schemas.project import ProjectCreate, ProjectUpdate
from sqlalchemy import or_
from app.models.project import ProjectModel
from app.models.project_members import ProjectMemberModel
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.core.exceptions import not_found, bad_request

def create_project_service(
    project_data: ProjectCreate, 
    current_data: UserModel, 
    db: Session
):
    if (not project_data.name.strip()):
        raise bad_request("Project name cannot be empty")
    
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
        .join(
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
        .join(
            ProjectMemberModel, 
            ProjectMemberModel.project_id == ProjectModel.id
        )
        .filter(
            ProjectModel.id == project_id,
            ProjectMemberModel.user_id == current_data.id
        )
        .first()
    )

    if (not project):
        raise not_found("Project not found or you are not a member of this project")

    members = (
        db.query(UserModel)
        .join(
            ProjectMemberModel,
            ProjectMemberModel.user_id == UserModel.id
        )
        .filter(
            ProjectMemberModel.project_id == project_id
        )
        .all()
    )

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "owner_id": project.owner_id,
        "created_at": project.created_at,
        "members": members
    }

def update_project_service(
    db: Session,
    current_data: UserModel,
    project_id: int,
    data: ProjectUpdate  
):
    project = (
        db.query(ProjectModel)
        .filter(
            project_id == ProjectModel.id,
            current_data.id == ProjectModel.owner_id
        )
        .first()
    )

    if (not project):
        raise not_found("Project not found or you are not the owner")

    project.name = data.name
    project.description = data.description

    db.commit()
    db.refresh(project)

    return project

def delete_project_service(
    db: Session,
    current_data: UserModel,
    project_id: int,  
):
    project = (
        db.query(ProjectModel)
        .filter(
            project_id == ProjectModel.id,
            current_data.id == ProjectModel.owner_id
        )
        .first()
    )

    if (not project):
        raise not_found("Project not found or you are not the owner")

    db.query(ProjectMemberModel).filter(
        ProjectMemberModel.project_id == project_id
    ).delete()

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }
