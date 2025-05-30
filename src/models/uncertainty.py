from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
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
    id: Mapped[int] = mapped_column(primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))

    probabilities: Mapped[str] = mapped_column(String, default="1")
    issue: Mapped["Issue"] = relationship("Issue", back_populates="uncertainty")

    def __init__(self, id: Optional[int], probabilities: str, issue_id: Optional[int]):
        if id is not None:
            self.id = id
        if issue_id:
            self.issue_id=issue_id
        self.probabilities = probabilities