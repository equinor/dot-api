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

if TYPE_CHECKING:
    from src.models.issue import Issue

class Uncertainty(Base):
    __tablename__ = "uncertainty"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    issue_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("issue.id"))

    probabilities: Mapped[str] = mapped_column(String, default="1")
    issue: Mapped["Issue"] = relationship("Issue", back_populates="uncertainty")

    def __init__(self, id: uuid.UUID, probabilities: str, issue_id: uuid.UUID):
        self.id = id
        self.issue_id=issue_id
        self.probabilities = probabilities
