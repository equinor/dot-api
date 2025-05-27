from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import Optional, TYPE_CHECKING
from src.models.base import Base
from src.models.base_auditable_entity import BaseAuditableEntity
from src.models.base import Base
from src.models.base_auditable_entity import BaseAuditableEntity
if TYPE_CHECKING:
    from src.models.opportunity import Opportunity
    from src.models.objective import Objective
    from models.scenario import Scenario

class Project(Base, BaseAuditableEntity):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), index=True)
    description: Mapped[str] = mapped_column(String(600))

    opportunities: Mapped[list["Opportunity"]] = relationship(
        "Opportunity",
        cascade="all, delete-orphan",
    )

    objectives: Mapped[list["Objective"]] = relationship(
        "Objective",
        cascade="all, delete-orphan",
    )

    scenarios: Mapped[list["Scenario"]] = relationship(
        "Scenario", 
        back_populates="project",
        cascade="all, delete-orphan",
    )

    def __init__(self, id: Optional[int], description: str, name: str, user_id: int, objectives: list["Objective"], opportunities: list["Opportunity"]):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.name = name
        self.description = description
        self.updated_by_id = user_id
        self.objectives = objectives
        self.opportunities = opportunities

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
