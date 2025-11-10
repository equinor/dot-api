import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from src.models.base import Base
from src.models.node import Node
from src.models.scenario import Scenario
from src.models.base_entity import BaseEntity


class Edge(Base, BaseEntity):
    __tablename__ = "edge"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)

    tail_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey(Node.id), index=True)
    head_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey(Node.id), index=True)
    scenario_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey(Scenario.id), index=True)

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

    def __init__(
        self,
        id: uuid.UUID,
        tail_node_id: uuid.UUID,
        head_node_id: uuid.UUID,
        scenario_id: uuid.UUID,
    ):
        self.id = id
        self.tail_id = tail_node_id
        self.head_id = head_node_id
        self.scenario_id = scenario_id
