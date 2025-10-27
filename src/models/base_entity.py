from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from datetime import timezone
from sqlalchemy import DateTime


class BaseEntity:
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            default=datetime.now(timezone.utc),
            onupdate=datetime.now(timezone.utc),
        )
        return mapped_column(
            DateTime(timezone=True),
            default=datetime.now(timezone.utc),
            onupdate=datetime.now(timezone.utc),
        )
