import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, UUID
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
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    issue_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("issue.id"))

    name: Mapped[str] = mapped_column(String, default="")
    issue: Mapped["Issue"] = relationship("Issue", back_populates="value_metric")

    def __init__(self, id: uuid.UUID, name: str, issue_id: uuid.UUID):
        self.id = id
        self.issue_id=issue_id
        self.name = name