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
from src.models.probability import Probability
from src.models.node import Node

class Issue(Base, BaseAuditableEntity):
    __tablename__ = "issue"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey(Scenario.id))
    node_id: Mapped[int] = mapped_column(ForeignKey(Node.id))
    decision_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Decision.id))
    probability_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Probability.id))

    type: Mapped[str] = mapped_column(String(30), default="Undecided")
    boundary: Mapped[str] = mapped_column(String(30), default="out")

    scenario: Mapped[Scenario] = relationship(Scenario, foreign_keys=[scenario_id], back_populates="issues")

    node: Mapped[Node] = relationship(
        Node, 
        foreign_keys=[node_id], 
    )

    decision: Mapped[Optional[Decision]] = relationship(
        Decision, 
        foreign_keys=[decision_id], 
        cascade="all, delete-orphan",
        single_parent=True,
    )
    probability: Mapped[Optional[Probability]] = relationship(
        Probability, 
        foreign_keys=[probability_id], 
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __init__(self, id: Optional[int], scenario_id: int, type: str, boundary: str, user_id: int, node_id: int, node: Node, decision_id: Optional[int] = None, probability_id: Optional[int] = None, decision: Optional[Decision] = None, probability: Optional[Probability] = None):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.scenario_id = scenario_id
        self.type = type
        self.boundary = boundary
        self.updated_by_id = user_id
        self.node_id = node_id
        self.Node = node
        self.decision_id = decision_id
        self.decision = decision
        self.probability_id = probability_id
        self.probability = probability