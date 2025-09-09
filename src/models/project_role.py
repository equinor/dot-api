import uuid
from src.models.guid import GUID
from src.models.base_entity import BaseEntity
from src.models.base_auditable_entity import BaseAuditableEntity
from sqlalchemy import   ForeignKey, String
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from sqlalchemy.event import listens_for
from src.constants import DatabaseConstants
from src.models.base import Base
from src.models.project import Project
from src.models.user import User

class ProjectRole(Base,BaseEntity, BaseAuditableEntity):
    __tablename__ = "project_role"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    project_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("project.id"), index=True) 
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)  
    role: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), nullable=False)
    project: Mapped[Project] = relationship("Project", back_populates="project_role", foreign_keys=[project_id])
    user: Mapped[User] = relationship("User", back_populates="project_role", foreign_keys=[user_id])

    def __init__(self,id: uuid.UUID, project_id: uuid.UUID, user_id: int, role: str):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.role = role
        self.updated_by_id = user_id

    def __repr__(self):
        return f"ProjectRole(id={self.id}, project_id={self.project_id}, user_id={self.user_id},role={self.role})"

@listens_for(ProjectRole, "before_insert")
def set_created_by_id(mapper, connection, target: ProjectRole): # type: ignore
    target.created_by_id = target.updated_by_id