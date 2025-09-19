from typing import TYPE_CHECKING
import uuid
from src.models.guid import GUID
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
    Session,
)
from src.models.base import Base
from sqlalchemy.event import listens_for
from src.models.guid import GUID

if TYPE_CHECKING:
    from src.models.node import Node
    from src.models.edge import Edge
    from src.models.objective import Objective
    from src.models.opportunity import Opportunity
    from src.models.issue import Issue
from src.models.project import Project
from src.models.base_entity import BaseEntity
from src.models.base_auditable_entity import BaseAuditableEntity
from src.constants import DatabaseConstants

class Scenario(Base, BaseEntity, BaseAuditableEntity):
    __tablename__ = "scenario"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Project.id), index=True)

    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), index=True, default="")

    is_default: Mapped[bool] = mapped_column(Boolean(), default=False)

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

    def __init__(self, id: uuid.UUID, name: str, project_id: uuid.UUID, user_id: int, objectives: list["Objective"], opportunities: list["Opportunity"], is_default: bool=False):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.updated_by_id = user_id
        self.objectives = objectives
        self.opportunities = opportunities
        self.is_default=is_default

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

def default_scenario_rule(connection, target: Scenario):
    """
    Ensure that after operation that project has 1 default scenario
    """

    # According to documentation sync engines should function asyncronously during an event
    session = Session(bind=connection)
    
    all_scenarios=session.query(Scenario).filter(
        Scenario.project_id == target.project_id,
    ).all()

    if len(all_scenarios)==0:
        return 
    
    if sum([x.is_default for x in all_scenarios]) != 1:
        raise ValueError(
                f"Project {target.project_id} must have exactly one default scenario."
            )

@listens_for(Scenario, "before_insert")
def set_created_by_id(mapper, connection, target: Scenario): # type: ignore
    target.created_by_id = target.updated_by_id

@listens_for(Scenario, "after_insert")
def ensure_one_default_scenario_on_insert(mapper, connection, target: Scenario):  # type: ignore
    default_scenario_rule(connection, target)


@listens_for(Scenario, "after_update")
def ensure_one_default_scenario_on_update(mapper, connection, target: Scenario):  # type: ignore
    default_scenario_rule(connection, target)

@listens_for(Scenario, "after_delete")
def ensure_one_default_scenario_on_update(mapper, connection, target: Scenario):  # type: ignore
    default_scenario_rule(connection, target)
