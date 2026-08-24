from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ProjectMemberBase(BaseModel):
    project_id: int
    user_id: int
    role: str = "MEMBER"


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMemberUpdate(BaseModel):
    role: str | None = None


class ProjectMemberDetailResponse(ProjectMemberBase):
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjectMemberResponse(BaseModel):
    user_id: int
    role: str

    model_config = ConfigDict(from_attributes=True)