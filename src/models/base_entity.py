from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import func


class BaseEntity:
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(default=func.now())

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(default=func.now(), onupdate=func.now())
