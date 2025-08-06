from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING, Optional
from src.models.base import Base
from src.constants import DatabaseConstants
from src.models.base_entity import BaseEntity
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
if TYPE_CHECKING:
    from models.project_contributors import ProjectContributors
    from models.project_owners import ProjectOwners
class User(Base, BaseEntity):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value))
    azure_id: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), unique=True)
    project_contributors: Mapped[list["ProjectContributors"]] = relationship(
        "ProjectContributors",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    project_owners: Mapped[list["ProjectOwners"]] = relationship(
        "ProjectOwners",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    def __init__(self, id: Optional[int], name: str, azure_id: str):
        if id is not None:
            self.id = id
        self.name = name
        self.azure_id = azure_id

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, azure_id: {self.azure_id}"
