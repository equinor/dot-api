from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
)
from src.models.base import Base

class Probability(Base):
    __tablename__ = "probability"
    id: Mapped[int] = mapped_column(primary_key=True)

    probabilities: Mapped[str] = mapped_column(String, default="1")

    def __init__(self, id: Optional[int], probabilities: str):
        if id is not None:
            self.id = id
        self.probabilities = probabilities