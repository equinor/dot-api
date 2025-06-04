from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models.base_auditable_entity import BaseAuditableEntity
from src.models.scenario import Scenario
from src.models.decision import Decision
from src.models.uncertainty import Uncertainty
from src.models.node import Node
from src.constants import DatabaseConstants

class Issue(Base, BaseAuditableEntity):
    __tablename__ = "issue"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey(Scenario.id))

    type: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), default="Undecided")
    boundary: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), default="out")

    scenario: Mapped[Scenario] = relationship(Scenario, foreign_keys=[scenario_id], back_populates="issues")

    node: Mapped[Node] = relationship(
        Node, 
        back_populates="issue",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    decision: Mapped[Optional[Decision]] = relationship(
        Decision, 
        back_populates="issue",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    uncertainty: Mapped[Optional[Uncertainty]] = relationship(
        Uncertainty, 
        back_populates="issue",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __init__(self, id: Optional[int], scenario_id: int, type: str, boundary: str, user_id: int, node: Node, decision: Optional[Decision] = None, uncertainty: Optional[Uncertainty] = None):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.scenario_id = scenario_id
        self.type = type
        self.boundary = boundary
        self.updated_by_id = user_id
        self.node = node
        self.decision = decision
        self.uncertainty = uncertainty