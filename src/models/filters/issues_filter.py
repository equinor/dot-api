import uuid
from typing import Optional
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore
from src.models.filters.base_filter import BaseFilter
from src.models import Issue, Scenario


class IssueFilter(BaseFilter):
    issue_id: Optional[uuid.UUID] = None
    scenario_id: Optional[uuid.UUID] = None
    project_id: Optional[uuid.UUID] = None
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    boundary: Optional[str] = None
    order: Optional[int] = None


def issue_conditions(filter: IssueFilter) -> list[_ColumnExpressionArgument[bool]]:
    conditions: list[_ColumnExpressionArgument[bool]] = []
    BaseFilter.add_condition(conditions, Issue.id == filter.issue_id if filter.issue_id else None)
    BaseFilter.add_condition(conditions, Issue.scenario_id == filter.scenario_id if filter.scenario_id else None)
    BaseFilter.add_condition(conditions, Issue.scenario.has(Scenario.project_id == filter.project_id) if filter.project_id else None)
    BaseFilter.add_condition(conditions, Issue.type == filter.type if filter.type else None)
    BaseFilter.add_condition(conditions, Issue.name.ilike(f"%{filter.name}%") if filter.name else None)
    BaseFilter.add_condition(conditions, Issue.description.ilike(f"%{filter.description}%") if filter.description else None)
    BaseFilter.add_condition(conditions, Issue.boundary == filter.boundary if filter.boundary else None)
    BaseFilter.add_condition(conditions, Issue.order == filter.order if filter.order is not None else None)
    return conditions
