from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models.scenario import Scenario
if TYPE_CHECKING:
    from src.models.edge import Edge
    from src.models.issue import Issue

class Node(Base):
    __tablename__ = "node"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey(Scenario.id))
    issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))

    name: Mapped[str] = mapped_column(String(60), index=True)

    scenario: Mapped[Scenario] = relationship(Scenario, foreign_keys=[scenario_id], back_populates="nodes")
    issue: Mapped["Issue"] = relationship(
        "Issue", 
        foreign_keys=[issue_id], 
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

    def __init__(self, id: Optional[int], scenario_id: int, name: str, issue_id: Optional[int]):
        if id is not None:
            self.id = id
        
        if issue_id:
            self.issue_id=issue_id

        self.scenario_id = scenario_id
        self.name = name

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