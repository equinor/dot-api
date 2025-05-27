from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models.node import Node
from src.models.scenario import Scenario

class Edge(Base):
    __tablename__ = "edge"

    id: Mapped[int] = mapped_column(primary_key=True)

    tail_id: Mapped[int] = mapped_column(ForeignKey(Node.id))
    head_id: Mapped[int] = mapped_column(ForeignKey(Node.id))
    scenario_id: Mapped[int] = mapped_column(ForeignKey(Scenario.id))

    scenario: Mapped[Scenario] = relationship(Scenario, foreign_keys=[scenario_id])

    tail_node: Mapped[Node] = relationship(
        Node, 
        primaryjoin=tail_id == Node.id, 
        back_populates="tail_edges",
    )

    head_node: Mapped[Node] = relationship(
        Node, 
        primaryjoin=head_id == Node.id, 
        back_populates="head_edges", 
    )

    def __init__(self, id: Optional[int], tail_node_id: int, head_node_id: int, scenario_id: int):
        if id is not None:
            self.id = id
        self.tail_id = tail_node_id
        self.head_id = head_node_id
        self.scenario_id = scenario_id