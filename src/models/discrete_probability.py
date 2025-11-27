import uuid
from typing import Optional, TYPE_CHECKING, Any
from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.engine import Connection
from src.models.base import Base
from src.models.base_entity import BaseEntity
from sqlalchemy.event import listens_for
from src.models.guid import GUID
if TYPE_CHECKING:
    from src.models.outcome import Outcome
    from src.models.option import Option
    from src.models.uncertainty import Uncertainty

class DiscreteProbabilityParentOutcome(Base):
    __tablename__ = "discrete_probability_parent_outcome"
    discrete_probability_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("discrete_probability.id"), primary_key=True)
    parent_outcome_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("outcome.id", ondelete="CASCADE"), primary_key=True)

    discrete_probability: Mapped["DiscreteProbability"] = relationship("DiscreteProbability", back_populates="parent_outcomes")
    parent_outcome: Mapped["Outcome"] = relationship("Outcome")

    def __init__(self, discrete_probability_id: uuid.UUID, parent_outcome_id: uuid.UUID):
        self.discrete_probability_id = discrete_probability_id
        self.parent_outcome_id = parent_outcome_id

class DiscreteProbabilityParentOption(Base):
    __tablename__ = "discrete_probability_parent_option"
    discrete_probability_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("discrete_probability.id"), primary_key=True)
    parent_option_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("option.id", ondelete="CASCADE"), primary_key=True)

    discrete_probability: Mapped["DiscreteProbability"] = relationship("DiscreteProbability", back_populates="parent_options")
    parent_option: Mapped["Option"] = relationship("Option", )

    def __init__(self, discrete_probability_id: uuid.UUID, parent_option_id: uuid.UUID):
        self.discrete_probability_id = discrete_probability_id
        self.parent_option_id = parent_option_id

class DiscreteProbability(Base, BaseEntity):
    __tablename__ = "discrete_probability"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    child_outcome_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("outcome.id", ondelete="CASCADE"), index=True)
    uncertainty_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("uncertainty.id"), index=True) # cascade delete handled in uncertainty model
    probability: Mapped[Optional[float]] = mapped_column(Float(precision=14), default=None, nullable=True)

    child_outcome: Mapped["Outcome"] = relationship("Outcome", foreign_keys=[child_outcome_id])
    uncertainty: Mapped["Uncertainty"] = relationship("Uncertainty", back_populates="discrete_probabilities", foreign_keys=[uncertainty_id])

    parent_outcomes: Mapped[list["DiscreteProbabilityParentOutcome"]] = relationship(
        "DiscreteProbabilityParentOutcome",
        back_populates="discrete_probability",
        cascade="all, delete-orphan"
    )

    parent_options: Mapped[list["DiscreteProbabilityParentOption"]] = relationship(
        "DiscreteProbabilityParentOption",
        back_populates="discrete_probability",
        cascade="all, delete-orphan"
    )

    def __init__(
        self,
        id: uuid.UUID,
        uncertainty_id: uuid.UUID,
        child_outcome_id: uuid.UUID,
        probability: Optional[float] = None,
        parent_outcomes: Optional[list["DiscreteProbabilityParentOutcome"]] = None,
        parent_options: Optional[list["DiscreteProbabilityParentOption"]] = None,
    ):
        self.id = id
        self.uncertainty_id = uncertainty_id
        self.child_outcome_id = child_outcome_id
        self.probability = probability
        self.parent_outcomes = parent_outcomes or []
        self.parent_options = parent_options or []

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DiscreteProbability):
            return False
        return (
            self.id == other.id and
            self.uncertainty_id == other.uncertainty_id and
            self.child_outcome_id == other.child_outcome_id and
            self.probability == other.probability and
            len(self.parent_outcomes) == len(other.parent_outcomes) and
            len(self.parent_options) == len(other.parent_options) and
            all(po1.parent_outcome_id == po2.parent_outcome_id for po1, po2 in zip(
                sorted(self.parent_outcomes, key=lambda x: x.parent_outcome_id), 
                sorted(other.parent_outcomes, key=lambda x: x.parent_outcome_id)
            )) and
            all(po1.parent_option_id == po2.parent_option_id for po1, po2 in zip(
                sorted(self.parent_options, key=lambda x: x.parent_option_id), 
                sorted(other.parent_options, key=lambda x: x.parent_option_id)
            ))
        )

    def __hash__(self) -> int:
        return hash(self.id)


# Event listeners to clean up orphaned DiscreteProbability records
@listens_for(DiscreteProbabilityParentOutcome, "after_delete")
def cleanup_orphaned_discrete_probability_after_outcome_delete(mapper: Any, connection: Connection, target: DiscreteProbabilityParentOutcome) -> None:
    _cleanup_orphaned_discrete_probability(connection, target.discrete_probability_id)


@listens_for(DiscreteProbabilityParentOption, "after_delete")
def cleanup_orphaned_discrete_probability_after_option_delete(mapper: Any, connection: Connection, target: DiscreteProbabilityParentOption) -> None:
    _cleanup_orphaned_discrete_probability(connection, target.discrete_probability_id)


def _cleanup_orphaned_discrete_probability(connection: Connection, discrete_probability_id: uuid.UUID) -> None:

    # First delete all parent outcome relationships
    connection.execute(
        DiscreteProbabilityParentOutcome.__table__.delete()
        .where(DiscreteProbabilityParentOutcome.discrete_probability_id == discrete_probability_id)
    )
    
    # Then delete all parent option relationships
    connection.execute(
        DiscreteProbabilityParentOption.__table__.delete()
        .where(DiscreteProbabilityParentOption.discrete_probability_id == discrete_probability_id)
    )
    
    # Finally delete the DiscreteProbability record itself
    connection.execute(
        DiscreteProbability.__table__.delete()
        .where(DiscreteProbability.id == discrete_probability_id)
    )
