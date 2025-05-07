from typing import Optional
from sqlalchemy.sql.schema import MetaData
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
)

Base = declarative_base()

class Decision(Base):
    __tablename__ = "decision"
    id: Mapped[int] = mapped_column(primary_key=True)

    options: Mapped[str] = mapped_column(String(60), default="")

    def __init__(self, id: Optional[int], options: str):
        if id is not None:
            self.id = id
        self.options = options

metadata: MetaData = Base.metadata