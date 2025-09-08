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

class Option(Base, BaseEntity):
    __tablename__ = "option"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    decision_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("decision.id"))

    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), default="")
    utility: Mapped[float] = mapped_column(Float(), default=0.0)

    # Relationships
    parent_outcomes: Mapped[list["OptionToOutcome"]] = relationship(
        "OptionToOutcome", foreign_keys=[OptionToOutcome.child_option_id]
    )  # Outcomes that this Option depends on

    parent_options: Mapped[list["OptionToOption"]] = relationship(
        "OptionToOption", foreign_keys=[OptionToOption.child_option_id]
    )  # Options that this Option depends on

    def __init__(
            self, id: uuid.UUID, decision_id: uuid.UUID, name: str, utility: float,
            parent_outcomes: list["OptionToOutcome"] = [], parent_options: list["OptionToOption"] = []
    ):
        self.id = id
        self.decision_id = decision_id
        self.name = name
        self.utility = utility

        self.parent_outcomes=parent_outcomes
        self.parent_options=parent_options
