import uuid
from sqlalchemy import String, ForeignKey, Float
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship,
)
from src.models.base import Base
from src.models.base_entity import BaseEntity
from src.constants import DatabaseConstants
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.outcome_to_option import OutcomeToOption
    from src.models.outcome_to_outcome import OutcomeToOutcome
    from src.models.option_to_outcome import OptionToOutcome
    from src.models.option_to_option import OptionToOption

class Outcome(Base, BaseEntity):
    __tablename__ = "outcome"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    uncertainty_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("uncertainty.id"))

    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), default="")
    probability: Mapped[float] = mapped_column(Float(), default=0.0)
    utility: Mapped[float] = mapped_column(Float(), default=0.0)

    # Relationships
    parent_outcomes: Mapped[list["OutcomeToOutcome"]] = relationship(
        "OutcomeToOutcome", foreign_keys=[OutcomeToOutcome.child_outcome_id]
    )  # Outcomes that this Outcome depends on

    parent_options: Mapped[list["OutcomeToOption"]] = relationship(
        "OutcomeToOption", foreign_keys=[OutcomeToOption.child_outcome_id]
    )  # Options that this Outcome depends on

    def __init__(
            self, id: uuid.UUID, uncertainty_id: uuid.UUID, name: str, probability: float, utility: float,
            parent_options: list["OutcomeToOption"] = [], parent_outcomes: list["OutcomeToOutcome"]=[]
        ):
        self.id = id
        self.uncertainty_id = uncertainty_id
        self.name = name
        self.probability = probability
        self.utility = utility

        self.parent_outcomes=parent_outcomes
        self.parent_options=parent_options