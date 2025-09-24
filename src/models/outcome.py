import uuid
from sqlalchemy import String, ForeignKey, Float
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from src.models.base import Base
from src.models.base_entity import BaseEntity
from src.constants import DatabaseConstants


class Outcome(Base, BaseEntity):
    __tablename__ = "outcome"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    uncertainty_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("uncertainty.id")
    )

    name: Mapped[str] = mapped_column(
        String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), default=""
    )

    probability: Mapped[float] = mapped_column(Float(), default=0.0)
    utility: Mapped[float] = mapped_column(Float(), default=0.0)

    def __init__(
        self,
        id: uuid.UUID,
        uncertainty_id: uuid.UUID,
        name: str,
        probability: float,
        utility: float,
    ):
        self.id = id
        self.uncertainty_id = uncertainty_id
        self.name = name
        self.probability = probability
        self.utility = utility
