import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from src.models.base import Base
from src.models.base_entity import BaseEntity
from src.models.outcome import Outcome
from src.models.outcome_probability import OutcomeProbability

if TYPE_CHECKING:
    from src.models.issue import Issue


class Uncertainty(Base, BaseEntity):
    __tablename__ = "uncertainty"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    issue_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("issue.id"), index=True)

    issue: Mapped["Issue"] = relationship("Issue", back_populates="uncertainty")

    outcomes: Mapped[list[Outcome]] = relationship("Outcome", cascade="all, delete-orphan")

    outcome_probabilities: Mapped[list[OutcomeProbability]] = relationship(
        "OutcomeProbability",
        cascade="all, delete-orphan",
        back_populates="uncertainty",
        foreign_keys="OutcomeProbability.uncertainty_id"
    )

    def __init__(self, id: uuid.UUID, issue_id: uuid.UUID, outcomes: list[Outcome], outcome_probabilities: Optional[list[OutcomeProbability]]=None):
        self.id = id
        self.issue_id = issue_id
        self.outcomes = outcomes
        if outcome_probabilities is not None:
            self.outcome_probabilities=outcome_probabilities
