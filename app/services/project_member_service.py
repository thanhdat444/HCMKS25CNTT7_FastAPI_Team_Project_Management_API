from sqlalchemy import or_
from app.models.project import ProjectModel
from app.models.project_members import ProjectMemberModel
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.core.exceptions import not_found, bad_request
from fastapi import HTTPException, status

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

def delete_member_project_service(
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

    if user_id == project.owner_id:
        raise bad_request("Owner cannot be removed from the project")

    member = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.project_id == project_id,
            ProjectMemberModel.user_id == user_id
        )
        .first()
    )

    if (not member):
        raise not_found("User is not a member of this project")

    db.delete(member)
    db.commit()

    return {
        "message": "Member removed successfully"
    }

def get_member_project_service(
    project_id: int,
    current_data: UserModel,
    db: Session      
):
    project = (
        db.query(ProjectModel)
        .outerjoin(
            ProjectMemberModel,
            ProjectMemberModel.project_id == ProjectModel.id
        )
        .filter(
            ProjectModel.id == project_id,
            or_(
                ProjectMemberModel.user_id == current_data.id,
                ProjectModel.owner_id == current_data.id
            )
        )
        .first()
    )

    if (not project):
        raise not_found("Project not found or you are not a member")

    members = (
        db.query(ProjectMemberModel)
        .filter(project_id == ProjectMemberModel.project_id)
        .all()
    )

    return members