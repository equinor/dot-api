import uuid
from typing import Optional
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore
from src.models.filters.base_filter import BaseFilter
from src.models import Scenario

class ScenarioFilter(BaseFilter):
    scenario_id: Optional[uuid.UUID] = None
    project_id: Optional[uuid.UUID] = None
    name: Optional[str] = None

def scenario_conditions(filter: ScenarioFilter) -> list[_ColumnExpressionArgument[bool]]:
    conditions: list[_ColumnExpressionArgument[bool]] = []
    BaseFilter.add_condition(conditions, Scenario.id == filter.scenario_id if filter.scenario_id else None)
    BaseFilter.add_condition(conditions, Scenario.project_id == filter.project_id if filter.project_id else None)
    BaseFilter.add_condition(conditions, Scenario.name.ilike(f"%{filter.name}%") if filter.name else None)
    return conditions