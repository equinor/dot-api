import uuid
from typing import Optional
from sqlalchemy.sql import ColumnElement, or_
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore
from src.models.filters.base_filter import BaseFilter
from src.models import Project

class ProjectFilter(BaseFilter):
    project_ids: Optional[list[uuid.UUID]] = None
    names: Optional[list[str]] = None
    descriptions: Optional[list[str]] = None
    accessing_user_id: Optional[int] = None

    def construct_filters(self) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []
        self.add_condition_for_property(self.project_ids, self._project_id_condition, conditions)
        self.add_condition_for_property(self.names, self._name_condition, conditions)
        self.add_condition_for_property(self.descriptions, self._description_condition, conditions)
        return conditions

    def construct_access_conditions(self) -> ColumnElement[bool]:
        conditions: list[_ColumnExpressionArgument[bool]] = [] 
        return or_(*conditions)

    # Static helper methods to encapsulate condition logic
    @staticmethod
    def _project_id_condition(project_id: uuid.UUID) -> ColumnElement[bool]:
        return Project.id == project_id

    @staticmethod
    def _name_condition(name: str) -> ColumnElement[bool]:
        return Project.name.ilike(f"%{name}%")

    @staticmethod
    def _description_condition(description: str) -> ColumnElement[bool]:
        return Project.description.ilike(f"%{description}%")