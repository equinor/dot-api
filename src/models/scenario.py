from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
if TYPE_CHECKING:
    from src.models.node import Node
    from src.models.edge import Edge
    from src.models.objective import Objective
    from src.models.opportunity import Opportunity
    from src.models.issue import Issue
from src.models.project import Project
from src.models.base_auditable_entity import BaseAuditableEntity

class Scenario(Base, BaseAuditableEntity):
    __tablename__ = "scenario"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey(Project.id), index=True)

    name: Mapped[str] = mapped_column(String(60), index=True, default="")

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

    def __init__(self, id: Optional[int], name: str, project_id: int, user_id: int, objectives: list["Objective"], opportunities: list["Opportunity"]):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.name = name
        self.project_id = project_id
        self.updated_by_id = user_id
        self.objectives = objectives
        self.opportunities = opportunities

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
