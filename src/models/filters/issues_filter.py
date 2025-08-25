import uuid
from typing import Optional
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore
from src.models.filters.base_filter import BaseFilter
from src.models import Issue, Scenario
from sqlalchemy.sql import ColumnElement

class IssueFilter(BaseFilter):
    issue_ids: Optional[list[uuid.UUID]] = None
    scenario_ids: Optional[list[uuid.UUID]] = None
    project_ids: Optional[list[uuid.UUID]] = None
    types: Optional[list[str]] = None
    names: Optional[list[str]] = None
    descriptions: Optional[list[str]] = None
    boundaries: Optional[list[str]] = None
    orders: Optional[list[int]] = None

    def construct_filters(self) -> list[ColumnElement[bool]]:
        # Initialize a list to hold all conditions
        conditions: list[ColumnElement[bool]] = []

        # Add conditions for each attribute
        self.add_condition_for_property(self.issue_ids, self._issue_id_condition, conditions)
        self.add_condition_for_property(self.scenario_ids, self._scenario_id_condition, conditions)
        self.add_condition_for_property(self.project_ids, self._project_id_condition, conditions)
        self.add_condition_for_property(self.types, self._type_condition, conditions)
        self.add_condition_for_property(self.names, self._name_condition, conditions)
        self.add_condition_for_property(self.descriptions, self._description_condition, conditions)
        self.add_condition_for_property(self.boundaries, self._boundary_condition, conditions)
        self.add_condition_for_property(self.orders, self._order_condition, conditions)

        return conditions

    # Static helper methods to encapsulate condition logic
    @staticmethod
    def _issue_id_condition(issue_id: uuid.UUID) -> ColumnElement[bool]:
        return Issue.id == issue_id

    @staticmethod
    def _scenario_id_condition(scenario_id: uuid.UUID) -> ColumnElement[bool]:
        return Issue.scenario_id == scenario_id

    @staticmethod
    def _project_id_condition(project_id: uuid.UUID) -> ColumnElement[bool]:
        return Issue.scenario.has(Scenario.project_id == project_id)

    @staticmethod
    def _type_condition(issue_type: str) -> ColumnElement[bool]:
        return Issue.type == issue_type

    @staticmethod
    def _name_condition(name: str) -> ColumnElement[bool]:
        return Issue.name.ilike(f"%{name}%")

    @staticmethod
    def _description_condition(description: str) -> ColumnElement[bool]:
        return Issue.description.ilike(f"%{description}%")

    @staticmethod
    def _boundary_condition(boundary: str) -> ColumnElement[bool]:
        return Issue.boundary == boundary

    @staticmethod
    def _order_condition(order: int) -> ColumnElement[bool]:
        return Issue.order == order
