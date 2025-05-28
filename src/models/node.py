from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models.base_auditable_entity import BaseAuditableEntity
from src.models.graph import Graph
from src.models.decision import Decision
from src.models.probability import Probability
if TYPE_CHECKING:
    from src.models.edge import Edge

class Node(Base, BaseAuditableEntity):
    __tablename__ = "node"

    id: Mapped[int] = mapped_column(primary_key=True)
    graph_id: Mapped[int] = mapped_column(ForeignKey(Graph.id))
    decision_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Decision.id))
    probability_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Probability.id))

    type: Mapped[str] = mapped_column(String(30), default="TBD")

    graph: Mapped[Graph] = relationship(Graph, foreign_keys=[graph_id], back_populates="nodes")

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

    higher_edges: Mapped[list["Edge"]] = relationship(
        "Edge",
        foreign_keys="[Edge.higher_id]",
        back_populates="higher_node",
        cascade="all, delete-orphan",
    )
    lower_edges: Mapped[list["Edge"]] = relationship(
        "Edge",
        foreign_keys="[Edge.lower_id]",
        back_populates="lower_node",
        cascade="all, delete-orphan",
    )

    def __init__(self, id: Optional[int], graph_id: int, type: str, user_id: int, decision_id: Optional[int] = None, probability_id: Optional[int] = None, decision: Optional[Decision] = None, probability: Optional[Probability] = None):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.graph_id = graph_id
        self.type = type
        self.decision_id = decision_id
        self.decision = decision
        self.probability_id = probability_id
        self.probability = probability
        self.updated_by_id = user_id

    def higher_neighbors(self) -> list["Node"]:
        # self.higher_edges: list["Edge"]
        try:
            return [x.higher_node for x in self.higher_edges]
        except:
            return []

    def lower_neighbors(self) -> list["Node"]:
        # self.lower_edges: list["Edge"]
        try:
            return [x.lower_node for x in self.lower_edges]
        except:
            return []