from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ProjectMemberBase(BaseModel):
    project_id: int
    user_id: int
    role: str


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMemberUpdate(ProjectMemberBase):
    role: str | None = None


class ProjectMemberResponse(ProjectMemberBase):
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)