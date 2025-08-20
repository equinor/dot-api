import uuid
from typing import Optional
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore
from src.models.filters.base_filter import BaseFilter
from src.models import Project

class ProjectFilter(BaseFilter):
    project_id: Optional[uuid.UUID] = None
    project_ids: Optional[list[uuid.UUID]] = None
    name: Optional[str] = None
    description: Optional[str] = None
    project_contributors: Optional[str] = None
    project_owners: Optional[str] = None
    accessing_user_id: Optional[int] = None

def project_conditions(filter: ProjectFilter) -> list[_ColumnExpressionArgument[bool]]:
    conditions: list[_ColumnExpressionArgument[bool]] = []
    BaseFilter.add_condition(conditions, Project.id == filter.project_id if filter.project_id else None)
    BaseFilter.add_condition(conditions, Project.id.in_(filter.project_ids) if filter.project_ids else None)
    BaseFilter.add_condition(conditions, Project.name.ilike(f"%{filter.name}%") if filter.name else None)
    BaseFilter.add_condition(conditions, Project.description.ilike(f"%{filter.description}%") if filter.description else None)
    return conditions

def project_access_conditions(filter: ProjectFilter) -> list[_ColumnExpressionArgument[bool]]:
    conditions: list[_ColumnExpressionArgument[bool]] = []
    BaseFilter.add_condition(
        conditions,
        Project.project_owners.any(user_id=filter.accessing_user_id) if filter.accessing_user_id else None
    )
    BaseFilter.add_condition(
        conditions,
        Project.project_contributors.any(user_id=filter.accessing_user_id) if filter.accessing_user_id else None
    )
    return conditions