from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from src.models.base import Base
from src.constants import DatabaseConstants

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value))
    azure_id: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), unique=True)

    def __init__(self, id: Optional[int], name: str, azure_id: str):
        if id is not None:
            self.id = id
        self.name = name
        self.azure_id = azure_id

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, azure_id: {self.azure_id}"
