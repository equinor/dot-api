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

class ValueMetric(Base):
    __tablename__ = "value_metric"
    id: Mapped[int] = mapped_column(primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))

    name: Mapped[str] = mapped_column(String, default="")
    issue: Mapped["Issue"] = relationship("Issue", back_populates="value_metric")

    def __init__(self, id: Optional[int], name: str, issue_id: Optional[int]):
        if id is not None:
            self.id = id
        if issue_id:
            self.issue_id=issue_id
        self.name = name