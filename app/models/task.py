from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text)

    assignee_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String(50), nullable=False, default="TODO")
    priority = Column(String(50), nullable=False)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("ProjectModel", back_populates="tasks")
    assignee = relationship("UserModel", back_populates="assigned_tasks")
