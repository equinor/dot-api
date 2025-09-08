import uuid
from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from src.models.guid import GUID
from src.models.base import Base
from src.models.base_entity import BaseEntity
from src.constants import DatabaseConstants
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models import Outcome, Option, Edge

class OptionToOption(Base, BaseEntity):
    __tablename__ = "option_to_option"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    parent_option_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("option.id"))
    child_option_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("option.id"))
    edge_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("edge.id"))

    # Relationships
    parent_option: Mapped["Option"] = relationship("Option", foreign_keys=[parent_option_id])
    child_option: Mapped["Option"] = relationship("Option", foreign_keys=[child_option_id])
    edge: Mapped["Edge"] = relationship(
        "Edge", 
        foreign_keys=[edge_id],
        back_populates="option_to_options",  # Add back_populates for bidirectional relationship
    )

    def __init__(self, id: uuid.UUID, parent_option_id: uuid.UUID, child_option_id: uuid.UUID, edge_id: uuid.UUID):
        self.id=id
        self.parent_option_id=parent_option_id
        self.child_option_id=child_option_id
        self.edge_id=edge_id

