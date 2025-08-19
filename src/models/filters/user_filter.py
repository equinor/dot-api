from typing import Optional
import uuid
from src.models.user import User
from src.models.filters.base_filter import BaseFilter
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore


class UserFilter(BaseFilter):
    id: Optional[int] = None
    name: Optional[str] = None
    azure_id: Optional[uuid.UUID] = None


def user_conditions(filter: UserFilter) -> list[_ColumnExpressionArgument[bool]]:
    conditions: list[_ColumnExpressionArgument[bool]] = []
    BaseFilter.add_condition(conditions, User.id == filter.id if filter.id else None)
    BaseFilter.add_condition(conditions, User.name.ilike(f"%{filter.name}%") if filter.name else None)
    BaseFilter.add_condition(conditions, User.azure_id == filter.azure_id if filter.azure_id else None)
    return conditions
