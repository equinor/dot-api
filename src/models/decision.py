from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
)
from src.models.base import Base

class Decision(Base):
    __tablename__ = "decision"
    id: Mapped[int] = mapped_column(primary_key=True)

    options: Mapped[str] = mapped_column(String(60), default="")

    def __init__(self, id: Optional[int], options: str):
        if id is not None:
            self.id = id
        self.options = options