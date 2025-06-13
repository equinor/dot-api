from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, INT
from sqlalchemy.orm import (
    Mapped, 
    relationship,
    mapped_column,
)
from src.models.base import Base
if TYPE_CHECKING:
    from src.models import Node

class NodeStyle(Base):
    __tablename__ = "node_style"
    id: Mapped[int] = mapped_column(primary_key=True)
    node_id: Mapped[int] = mapped_column(ForeignKey("node.id"))

    x_position: Mapped[int] = mapped_column(INT)
    y_position: Mapped[int] = mapped_column(INT)

    node: Mapped["Node"] = relationship("Node", back_populates="node_style")

    def __init__(self, id: Optional[int], node_id: Optional[int], x_position: int = 0, y_position: int = 0):
        if id is not None:
            self.id = id
        if node_id:
            self.node_id=node_id
        self.x_position=x_position
        self.y_position=y_position
