import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.models.base_entity import BaseEntity
from src.models.guid import GUID
if TYPE_CHECKING:
    from src.models.outcome import Outcome
    from src.models.option import Option
    from src.models.uncertainty import Uncertainty

class OutcomeProbabilityParentOutcome(Base):
    __tablename__ = "outcome_probability_parent_outcome"
    outcome_probability_id = mapped_column(GUID(), ForeignKey("outcome_probability.id"), primary_key=True)
    parent_outcome_id = mapped_column(GUID(), ForeignKey("outcome.id"), primary_key=True)

    outcome_probability: Mapped["OutcomeProbability"] = relationship("OutcomeProbability", back_populates="parent_outcomes")
    parent_outcome: Mapped["Outcome"] = relationship("Outcome")

    def __init__(self, outcome_probability_id: uuid.UUID, parent_outcome_id: uuid.UUID):
        self.outcome_probability_id = outcome_probability_id
        self.parent_outcome_id = parent_outcome_id

class OutcomeProbabilityParentOption(Base):
    __tablename__ = "outcome_probability_parent_option"
    outcome_probability_id = mapped_column(GUID(), ForeignKey("outcome_probability.id"), primary_key=True)
    parent_option_id = mapped_column(GUID(), ForeignKey("option.id"), primary_key=True)

    outcome_probability: Mapped["OutcomeProbability"] = relationship("OutcomeProbability", back_populates="parent_options")
    parent_option: Mapped["Option"] = relationship("Option")

    def __init__(self, outcome_probability_id: uuid.UUID, parent_option_id: uuid.UUID):
        self.outcome_probability_id = outcome_probability_id
        self.parent_option_id = parent_option_id

class OutcomeProbability(Base, BaseEntity):
    __tablename__ = "outcome_probability"
    id = mapped_column(GUID(), primary_key=True)
    child_outcome_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("outcome.id"), index=True)
    uncertainty_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("uncertainty.id"), index=True)
    probability: Mapped[float] = mapped_column(Float(), default=0.0)

    child_outcome: Mapped["Outcome"] = relationship("Outcome", foreign_keys=[child_outcome_id])
    uncertainty: Mapped["Uncertainty"] = relationship("Uncertainty", back_populates="outcome_probabilities", foreign_keys=[uncertainty_id])

    parent_outcomes: Mapped[list["OutcomeProbabilityParentOutcome"]] = relationship(
        "OutcomeProbabilityParentOutcome",
        back_populates="outcome_probability",
        cascade="all, delete-orphan"
    )

    parent_options: Mapped[list["OutcomeProbabilityParentOption"]] = relationship(
        "OutcomeProbabilityParentOption",
        back_populates="outcome_probability",
        cascade="all, delete-orphan"
    )

    def __init__(
        self,
        id: uuid.UUID,
        uncertainty_id: uuid.UUID,
        child_outcome_id: uuid.UUID,
        probability: float = 0.0,
        parent_outcomes: Optional[list["OutcomeProbabilityParentOutcome"]] = None,
        parent_options: Optional[list["OutcomeProbabilityParentOption"]] = None,
    ):
        self.id = id
        self.uncertainty_id = uncertainty_id
        self.child_outcome_id = child_outcome_id
        self.probability = probability
        self.parent_outcomes = parent_outcomes or []
        self.parent_options = parent_options or []
