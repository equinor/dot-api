from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import Optional, TYPE_CHECKING
from src.models.base import Base
from src.models.base_auditable_entity import BaseAuditableEntity
from src.models.base import Base
from src.models.base_auditable_entity import BaseAuditableEntity
from src.constants import DatabaseConstants
if TYPE_CHECKING:
    from models.scenario import Scenario

class Project(Base, BaseAuditableEntity):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), index=True)
    description: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_LONG_STRING_LENGTH.value))

    scenarios: Mapped[list["Scenario"]] = relationship(
        "Scenario", 
        back_populates="project",
        cascade="all, delete-orphan",
    )

    def __init__(self, id: Optional[int], description: str, name: str, user_id: int, scenarios: Optional[list["Scenario"]]):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id
            
        if scenarios is not None:
            self.scenarios=scenarios

        self.name = name
        self.description = description
        self.updated_by_id = user_id

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
