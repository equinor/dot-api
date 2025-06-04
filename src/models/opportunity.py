from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)
from src.models.base import Base
from src.models.base_auditable_entity import BaseAuditableEntity
from src.models.scenario import Scenario
from src.constants import DatabaseConstants

class Opportunity(Base, BaseAuditableEntity):
    __tablename__ = "opportunity"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey(Scenario.id), index=True)

    name: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), index=True, default="")
    description: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_LONG_STRING_LENGTH.value), default="")

    scenario: Mapped[Scenario] = relationship(
        Scenario, 
        foreign_keys=[scenario_id],
        back_populates="opportunities",
    )

    def __init__(self, id: Optional[int], scenario_id: int, description: str, name: str, user_id: int):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.scenario_id = scenario_id
        self.name = name
        self.description = description
        self.updated_by_id = user_id

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"