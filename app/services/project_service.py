from app.schemas.project import ProjectCreate, ProjectUpdate
from sqlalchemy import or_
from app.models.project import ProjectModel
from app.models.project_members import ProjectMemberModel
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.core.exceptions import not_found
from fastapi import HTTPException, status

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

    if (not project):
        raise not_found("Project not found or you are not a member of this project")

    return project

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

def add_member_project_service(
    db: Session,
    current_data: UserModel,
    project_id: int,
    user_id: int
):
    project = (
        db.query(ProjectModel)
        .filter(
            current_data.id == ProjectModel.owner_id,
            project_id == ProjectModel.id
        )
        .first()
    )

    if (not project):
        raise not_found("Project not found or you are not the owner")

    user = (
        db.query(UserModel)
        .filter(user_id == UserModel.id)
        .first()
    )

    if (not user):
        raise not_found("User not found")

    member = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.user_id == user_id,
            ProjectMemberModel.project_id == project_id
        )
        .first()
    )

    if (member):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this project"
        )

    new_user = ProjectMemberModel(
        project_id = project.id,
        user_id = user.id,
        role = "MEMBER"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user