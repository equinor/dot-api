import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, INT
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from src.models.base import Base
from src.models.base_entity import BaseEntity

if TYPE_CHECKING:
    from src.models import Node


class NodeStyle(Base, BaseEntity):
    __tablename__ = "node_style"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    node_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("node.id"), index=True)

    x_position: Mapped[int] = mapped_column(INT)
    y_position: Mapped[int] = mapped_column(INT)
    width: Mapped[int] = mapped_column(INT)
    height: Mapped[int] = mapped_column(INT)

    node: Mapped["Node"] = relationship("Node", back_populates="node_style")

    def __init__(
        self,
        id: uuid.UUID,
        node_id: Optional[uuid.UUID],
        width: int,
        height: int,
        x_position: int = 0,
        y_position: int = 0,
    ):
        self.id = id
        if node_id:
            self.node_id = node_id
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
