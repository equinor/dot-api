import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Float
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.event import listens_for
from src.models.base import Base
from src.models.base_entity import BaseEntity
from src.constants import DatabaseConstants

if TYPE_CHECKING:
    from src.models.discrete_probability import DiscreteProbabilityParentOption


class Option(Base, BaseEntity):
    __tablename__ = "option"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    decision_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("decision.id"), index=True)

    name: Mapped[str] = mapped_column(
        String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), default=""
    )

    utility: Mapped[float] = mapped_column(Float(), default=0.0)

    discrete_probability_parent_options: Mapped[list["DiscreteProbabilityParentOption"]] = relationship(
        "DiscreteProbabilityParentOption",
        back_populates="parent_option",
        cascade="all, delete-orphan",
    )

    def __init__(self, id: uuid.UUID, decision_id: uuid.UUID, name: str, utility: float):
        self.id = id
        self.decision_id = decision_id
        self.name = name
        self.utility = utility
