import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import (
    Mapped, 
    relationship,
    mapped_column,
)
from src.models.base import Base
from src.constants import DatabaseConstants
if TYPE_CHECKING:
    from src.models.issue import Issue

class Utility(Base):
    __tablename__ = "utility"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    issue_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("issue.id"))

    values: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), default="")
    issue: Mapped["Issue"] = relationship("Issue", back_populates="utility")

    def __init__(self, id: uuid.UUID, values: str, issue_id: uuid.UUID):
        self.id = id
        self.issue_id=issue_id
        self.values = values