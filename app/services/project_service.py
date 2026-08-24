from app.schemas.project import ProjectCreate

from app.models.project import ProjectModel
from app.models.project_members import ProjectMemberModel
from app.models.user import UserModel
from sqlalchemy.orm import Session

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