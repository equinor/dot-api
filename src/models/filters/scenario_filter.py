import uuid
from typing import Optional
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore
from src.models.filters.base_filter import BaseFilter
from src.models import Scenario
from sqlalchemy.sql import ColumnElement

class ScenarioFilter(BaseFilter):
    scenario_ids: Optional[list[uuid.UUID]] = None
    project_ids: Optional[list[uuid.UUID]] = None
    names: Optional[list[str]] = None

    def construct_filters(self) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []
        self.add_condition_for_property(self.scenario_ids, self._scenario_id_condition, conditions)
        self.add_condition_for_property(self.project_ids, self._project_id_condition, conditions)
        self.add_condition_for_property(self.names, self._name_condition, conditions)
        return conditions

    # Static helper methods to encapsulate condition logic
    @staticmethod
    def _scenario_id_condition(scenario_id: uuid.UUID) -> ColumnElement[bool]:
        return Scenario.id == scenario_id

    @staticmethod
    def _project_id_condition(project_id: uuid.UUID) -> ColumnElement[bool]:
        return Scenario.project_id == project_id

    @staticmethod
    def _name_condition(name: str) -> ColumnElement[bool]:
        return Scenario.name.ilike(f"%{name}%")
