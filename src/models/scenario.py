from typing import TYPE_CHECKING
import uuid
from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from sqlalchemy.event import listens_for

if TYPE_CHECKING:
    from src.models.node import Node
    from src.models.edge import Edge
    from src.models.objective import Objective
    from src.models.opportunity import Opportunity
    from src.models.issue import Issue
from src.models.project import Project
from src.models.base_auditable_entity import BaseAuditableEntity
from src.constants import DatabaseConstants

class Scenario(Base, BaseAuditableEntity):
    __tablename__ = "scenario"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Project.id), index=True)

    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), index=True, default="")

    project: Mapped[Project] = relationship(Project, foreign_keys=[project_id])

    opportunities: Mapped[list["Opportunity"]] = relationship(
        "Opportunity",
        cascade="all, delete-orphan",
    )

    objectives: Mapped[list["Objective"]] = relationship(
        "Objective",
        cascade="all, delete-orphan",
    )

    issues: Mapped[list["Issue"]] = relationship(
        "Issue",
        cascade="all, delete-orphan",
    )

    nodes: Mapped[list["Node"]] = relationship(
        "Node", 
        back_populates="scenario", 
        cascade="all, delete-orphan",
    )

    edges: Mapped[list["Edge"]] = relationship(
        "Edge",
        cascade="all, delete-orphan",
    )

    def __init__(self, id: uuid.UUID, name: str, project_id: uuid.UUID, user_id: int, objectives: list["Objective"], opportunities: list["Opportunity"]):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.updated_by_id = user_id
        self.objectives = objectives
        self.opportunities = opportunities

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

@listens_for(Scenario, "before_insert")
def set_created_by_id(mapper, connection, target: Scenario): # type: ignore
    target.created_by_id = target.updated_by_id