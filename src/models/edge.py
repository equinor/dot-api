from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models.node import Node
from src.models.graph import Graph

class Edge(Base):
    __tablename__ = "edge"

    id: Mapped[int] = mapped_column(primary_key=True)

    lower_id: Mapped[int] = mapped_column(ForeignKey(Node.id))
    higher_id: Mapped[int] = mapped_column(ForeignKey(Node.id))
    graph_id: Mapped[int] = mapped_column(ForeignKey(Graph.id))

    graph: Mapped[Graph] = relationship(Graph, foreign_keys=[graph_id])

    lower_node: Mapped[Node] = relationship(
        Node, 
        primaryjoin=lower_id == Node.id, 
        back_populates="lower_edges",
    )

    higher_node: Mapped[Node] = relationship(
        Node, 
        primaryjoin=higher_id == Node.id, 
        back_populates="higher_edges", 
    )

    def __init__(self, id: Optional[int], lower_node_id: int, higher_node_id: int, graph_id: int):
        if id is not None:
            self.id = id
        self.lower_id = lower_node_id
        self.higher_id = higher_node_id
        self.graph_id = graph_id