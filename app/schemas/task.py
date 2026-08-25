from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Literal


class TaskBase(BaseModel):
    project_id: int
    title: str
    description: str | None = None
    assignee_id: int | None = None
    status: str
    priority: str
    due_date: datetime | None = None


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: str
    due_date: datetime | None = None
    priority: Literal["LOW", "MEDIUM", "HIGH"]


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    status: Literal["TODO", "IN_PROGRESS", "DONE"] | None = None
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None
    due_date: datetime | None = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)