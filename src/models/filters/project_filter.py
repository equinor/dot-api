import uuid
from typing import Optional
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore
from src.models.filters.base_filter import BaseFilter
from src.models import Project

class ProjectFilter(BaseFilter):
    project_id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None

def project_conditions(filter: ProjectFilter) -> list[_ColumnExpressionArgument[bool]]:
    conditions: list[_ColumnExpressionArgument[bool]] = []
    BaseFilter.add_condition(conditions, Project.id == filter.project_id if filter.project_id else None)
    BaseFilter.add_condition(conditions, Project.name.ilike(f"%{filter.name}%") if filter.name else None)
    BaseFilter.add_condition(conditions, Project.description.ilike(f"%{filter.description}%") if filter.description else None)
    return conditions