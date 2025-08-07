from typing import TYPE_CHECKING
import uuid
from src.models.base_entity import BaseEntity
from src.models.base_auditable_entity import BaseAuditableEntity
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models.project import Project
from src.models.user import User

class ProjectContributors(Base,BaseEntity, BaseAuditableEntity):
    __tablename__ = "project_contributors"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    project: Mapped[Project] = relationship("Project", back_populates="project_contributors", foreign_keys=[project_id])
    user: Mapped[User] = relationship("User", back_populates="project_contibutors", foreign_keys=[user_id])

    def __init__(self, project_id: uuid.UUID, user_id: int):
        self.project_id = project_id
        self.user_id = user_id

    def __repr__(self):
        return f"ProjectContributors(project_id={self.project_id}, user_id={self.user_id})"
   