import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models.scenario import Scenario
from src.models.base_entity import BaseEntity
from src.constants import DatabaseConstants
if TYPE_CHECKING:
    from src.models import Edge
    from src.models import Issue
    from src.models import NodeStyle

class Node(Base, BaseEntity):
    __tablename__ = "node"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    scenario_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey(Scenario.id))
    issue_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("issue.id"))

    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), index=True)

    scenario: Mapped[Scenario] = relationship(Scenario, foreign_keys=[scenario_id], back_populates="nodes")
    issue: Mapped["Issue"] = relationship("Issue", back_populates="node")

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

    node_style: Mapped["NodeStyle"] = relationship(
        "NodeStyle",
        back_populates="node",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __init__(self, id: uuid.UUID, scenario_id: uuid.UUID, name: str, issue_id: Optional[uuid.UUID], node_style: Optional["NodeStyle"]):
        self.id = id
        
        self.scenario_id = scenario_id
        self.name = name
        
        if issue_id:
            self.issue_id=issue_id

        if node_style:
            self.node_style=node_style

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
