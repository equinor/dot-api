from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional
from src.models.base import Base
from src.constants import DatabaseConstants
from src.models.base_entity import BaseEntity


if TYPE_CHECKING:
    from src.models.project_role import ProjectRole


class User(Base, BaseEntity):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value))
    azure_id: Mapped[str] = mapped_column(
        String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), unique=True
    )

    project_role: Mapped[list["ProjectRole"]] = relationship(
        "ProjectRole",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="ProjectRole.user_id",
    )

    def __init__(
        self,
        id: Optional[int],
        name: str,
        azure_id: str,
        project_role: Optional[list["ProjectRole"]] = None,
    ):
        if id is not None:
            self.id = id
        self.name = name
        self.azure_id = azure_id
        if project_role is not None:
            self.project_role = project_role

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, azure_id: {self.azure_id}, project_role: {self.project_role}"
