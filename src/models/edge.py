import uuid
from sqlalchemy import ForeignKey
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models import (
    Node,
    Scenario,
    OptionToOption,
    OptionToOutcome, 
    OutcomeToOutcome,
    OutcomeToOption,
)

from src.models.base_entity import BaseEntity

class Edge(Base, BaseEntity):
    __tablename__ = "edge"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)

    tail_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey(Node.id))
    head_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey(Node.id))
    scenario_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey(Scenario.id))

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

    option_to_options: Mapped[list["OptionToOption"]] = relationship(
        "OptionToOption",
        back_populates="edge",
        cascade="all, delete-orphan",
    )

    option_to_outcomes: Mapped[list["OptionToOutcome"]] = relationship(
        "OptionToOutcome",
        back_populates="edge",
        cascade="all, delete-orphan",
    )

    outcome_to_outcomes: Mapped[list["OutcomeToOutcome"]] = relationship(
        "OutcomeToOutcome",
        back_populates="edge",
        cascade="all, delete-orphan",
    )

    outcome_to_options: Mapped[list["OutcomeToOption"]] = relationship(
        "OutcomeToOption",
        back_populates="edge",
        cascade="all, delete-orphan",
    )


    def __init__(self, id: uuid.UUID, tail_node_id: uuid.UUID, head_node_id: uuid.UUID, scenario_id: uuid.UUID):
        self.id = id
        self.tail_id = tail_node_id
        self.head_id = head_node_id
        self.scenario_id = scenario_id