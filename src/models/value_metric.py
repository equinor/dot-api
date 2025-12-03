import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from src.models.guid import GUID
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from src.models.base_entity import BaseEntity
from src.models.base import Base

if TYPE_CHECKING:
    from src.models import Scenario


class ValueMetric(Base, BaseEntity):
    __tablename__ = "value_metric"
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    scenario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Scenario.id"), index=True)

    name: Mapped[str] = mapped_column(String, default="")
    scenario: Mapped["Scenario"] = relationship(
        "Scenario", 
        foreign_keys=[scenario_id],
        back_populates="value_metrics"
    )

    def __init__(self, id: uuid.UUID, name: str, scenario_id: uuid.UUID):
        self.id = id
        self.scenario_id = scenario_id
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValueMetric):
            return False
        return (
            self.id == other.id and
            self.scenario_id == other.scenario_id and
            self.name == other.name
        )

    def __hash__(self) -> int:
        return hash(uuid.uuid4())
