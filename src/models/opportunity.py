from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models.base_auditable_entity import BaseAuditableEntity
from src.models.project import Project

class Opportunity(Base, BaseAuditableEntity):
    __tablename__ = "opportunity"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey(Project.id), index=True)

    name: Mapped[str] = mapped_column(String(60), index=True, default="")
    description: Mapped[str] = mapped_column(String(600), default="")

    project: Mapped[Project] = relationship(
        Project, 
        foreign_keys=[project_id],
        back_populates="opportunities",
    )

    def __init__(self, id: Optional[int], project_id: int, description: str, name: str, user_id: int):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.project_id = project_id
        self.name = name
        self.description = description
        self.updated_by_id = user_id

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"