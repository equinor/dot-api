import uuid
from typing import Optional
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore
from src.models.filters.base_filter import BaseFilter
from src.models import Node, Scenario

class NodeFilter(BaseFilter):
    node_id: Optional[uuid.UUID] = None
    issue_id: Optional[uuid.UUID] = None
    scenario_id: Optional[uuid.UUID] = None
    project_id: Optional[uuid.UUID] = None
    name: Optional[str] = None

def node_conditions(filter: NodeFilter) -> list[_ColumnExpressionArgument[bool]]:
    conditions: list[_ColumnExpressionArgument[bool]] = []
    BaseFilter.add_condition(conditions, Node.id == filter.node_id if filter.node_id else None)
    BaseFilter.add_condition(conditions, Node.issue_id == filter.issue_id if filter.issue_id else None)
    BaseFilter.add_condition(conditions, Node.scenario_id == filter.scenario_id if filter.scenario_id else None)
    BaseFilter.add_condition(conditions, Node.scenario.has(Scenario.project_id == filter.project_id) if filter.project_id else None)
    BaseFilter.add_condition(conditions, Node.name.ilike(f"%{filter.name}%") if filter.name else None)
    return conditions