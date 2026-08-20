from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TaskBase(BaseModel):
    project_id: int
    title: str
    description: str | None = None
    assignee_id: int | None = None
    status: str
    priority: str
    due_date: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)