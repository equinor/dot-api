from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from sqlalchemy import ForeignKey
from src.models.user import User


class BaseAuditableEntity:

    @declared_attr
    def created_by_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey(User.id))

    @declared_attr
    def updated_by_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey(User.id))

    @declared_attr
    def created_by(cls) -> Mapped["User"]:
        return relationship(User, foreign_keys=[cls.created_by_id]) # type: ignore # reason: declared_attr does not check in time

    @declared_attr
    def updated_by(cls) -> Mapped["User"]:
        return relationship(User, foreign_keys=[cls.updated_by_id]) # type: ignore # reason: declared_attr does not check in time