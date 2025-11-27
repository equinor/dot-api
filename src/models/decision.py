import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from src.models.base import Base
from src.models.base_entity import BaseEntity
from src.models.option import Option
from src.constants import (
    DatabaseConstants,
    DecisionHierarchy,
)

if TYPE_CHECKING:
    from src.models.issue import Issue


class Decision(Base, BaseEntity):
    __tablename__ = "decision"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    issue_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("issue.id"), index=True)

    issue: Mapped["Issue"] = relationship("Issue", back_populates="decision")
    options: Mapped[list[Option]] = relationship("Option", cascade="all, delete-orphan")
    type: Mapped[str] = mapped_column(
        String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value),
        default=DecisionHierarchy.FOCUS.value,
    )

    def __init__(self, id: uuid.UUID, options: list[Option], issue_id: uuid.UUID, type: str = DecisionHierarchy.FOCUS.value):
        self.id = id
        self.issue_id = issue_id
        self.options = options
        self.type = type

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Decision):
            return False
        return (
            self.id == other.id and
            self.issue_id == other.issue_id and
            self.type == other.type and
            len(self.options) == len(other.options) and
            all(opt1 == opt2 for opt1, opt2 in zip(sorted(self.options, key=lambda x: x.id), sorted(other.options, key=lambda x: x.id)))
        )

    def __hash__(self) -> int:
        return hash(self.id)
