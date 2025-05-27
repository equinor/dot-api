from typing import Optional, TYPE_CHECKING
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
if TYPE_CHECKING:
    from src.models.edge import Edge

class Node(Base, BaseAuditableEntity):
    __tablename__ = "node"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey(Scenario.id))
    decision_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Decision.id))
    probability_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Probability.id))

    type: Mapped[str] = mapped_column(String(30), default="TBD")

    scenario: Mapped[Scenario] = relationship(Scenario, foreign_keys=[scenario_id], back_populates="nodes")

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

    head_edges: Mapped[list["Edge"]] = relationship(
        "Edge",
        foreign_keys="[Edge.head_id]",
        back_populates="head_node",
        cascade="all, delete-orphan",
    )
    tail_edges: Mapped[list["Edge"]] = relationship(
        "Edge",
        foreign_keys="[Edge.tail_id]",
        back_populates="tail_node",
        cascade="all, delete-orphan",
    )

    def __init__(self, id: Optional[int], scenario_id: int, type: str, user_id: int, decision_id: Optional[int] = None, probability_id: Optional[int] = None, decision: Optional[Decision] = None, probability: Optional[Probability] = None):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.scenario_id = scenario_id
        self.type = type
        self.decision_id = decision_id
        self.decision = decision
        self.probability_id = probability_id
        self.probability = probability
        self.updated_by_id = user_id

    def head_neighbors(self) -> list["Node"]:
        try:
            return [x.head_node for x in self.head_edges]
        except:
            return []

    def tail_neighbors(self) -> list["Node"]:
        try:
            return [x.tail_node for x in self.tail_edges]
        except:
            return []