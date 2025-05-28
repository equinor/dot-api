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

class Decision(Base):
    __tablename__ = "decision"
    id: Mapped[int] = mapped_column(primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))

    options: Mapped[str] = mapped_column(String(60), default="")
    issue: Mapped["Issue"] = relationship("Issue", back_populates="decision")

    def __init__(self, id: Optional[int], options: str, issue_id: Optional[int]):
        if id is not None:
            self.id = id
        if issue_id:
            self.issue_id=issue_id
        self.options = options