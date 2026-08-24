from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime, timezone

class ProjectMemberModel(Base):
    __tablename__ = "project_members"

    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    role = Column(String(50), nullable=False, default="MEMBER")

    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("ProjectModel", back_populates="members")
    user = relationship("UserModel", back_populates="project_members")