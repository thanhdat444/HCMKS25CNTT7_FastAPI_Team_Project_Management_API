from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: str | None = None
    description: str | None = None


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjectMemberResponse(BaseModel):
    id: int
    fullname: str

    model_config = ConfigDict(from_attributes=True)

class ProjecDetailtResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    members: list[ProjectMemberResponse]

    model_config = ConfigDict(from_attributes=True)