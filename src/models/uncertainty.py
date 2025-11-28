import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, Boolean
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from src.models.base import Base
from src.models.base_entity import BaseEntity
from src.models.outcome import Outcome
from src.models.discrete_probability import DiscreteProbability

if TYPE_CHECKING:
    from src.models.issue import Issue


class Uncertainty(Base, BaseEntity):
    __tablename__ = "uncertainty"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    issue_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("issue.id"), index=True)
    is_key: Mapped[bool] = mapped_column(Boolean, default=True)

    issue: Mapped["Issue"] = relationship("Issue", back_populates="uncertainty")

    outcomes: Mapped[list[Outcome]] = relationship("Outcome", cascade="all, delete-orphan")

    discrete_probabilities: Mapped[list[DiscreteProbability]] = relationship(
        "DiscreteProbability",
        cascade="all, delete-orphan",
        back_populates="uncertainty",
        foreign_keys="DiscreteProbability.uncertainty_id"
    )

    def __init__(self, id: uuid.UUID, issue_id: uuid.UUID, outcomes: list[Outcome], is_key: bool = True, discrete_probabilities: Optional[list[DiscreteProbability]]=None):
        self.id = id
        self.issue_id = issue_id
        self.outcomes = outcomes
        self.is_key = is_key
        if discrete_probabilities is not None:
            self.discrete_probabilities=discrete_probabilities

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Uncertainty):
            return False
        return (
            self.id == other.id and
            self.issue_id == other.issue_id and
            self.is_key == other.is_key and
            len(self.outcomes) == len(other.outcomes) and
            all(out1 == out2 for out1, out2 in zip(sorted(self.outcomes, key=lambda x: x.id), sorted(other.outcomes, key=lambda x: x.id))) and
            len(self.discrete_probabilities) == len(other.discrete_probabilities) and
            all(dp1 == dp2 for dp1, dp2 in zip(sorted(self.discrete_probabilities, key=lambda x: x.id), sorted(other.discrete_probabilities, key=lambda x: x.id)))
        )

    def __hash__(self) -> int:
        return hash(uuid.uuid4())
