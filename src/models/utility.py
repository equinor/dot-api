import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from src.models.base import Base
from src.constants import DatabaseConstants
from src.models.base_entity import BaseEntity

if TYPE_CHECKING:
    from src.models.issue import Issue
    from src.models.discrete_utility import DiscreteUtility


class Utility(Base, BaseEntity):
    __tablename__ = "utility"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    issue_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("issue.id"), index=True)

    values: Mapped[str] = mapped_column(
        String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), default=""
    )
    issue: Mapped["Issue"] = relationship("Issue", back_populates="utility")
    discrete_utilities: Mapped[list["DiscreteUtility"]] = relationship(
        "DiscreteUtility",
        back_populates="utility",
        cascade="all, delete-orphan",
        foreign_keys="[DiscreteUtility.utility_id]"
    )

    def __init__(self, id: uuid.UUID, values: str, issue_id: uuid.UUID):
        self.id = id
        self.issue_id = issue_id
        self.values = values

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Utility):
            return False
        return (
            self.id == other.id and
            self.issue_id == other.issue_id and
            self.values == other.values
        )

    def __hash__(self) -> int:
        return hash(uuid.uuid4())
