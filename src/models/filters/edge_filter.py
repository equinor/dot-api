from typing import Optional
import uuid
from src.models.edge import Edge
from src.models.node import Node
from src.models.issue import Issue
from src.models.filters.base_filter import BaseFilter
from sqlalchemy.sql import ColumnElement


class EdgeFilter(BaseFilter):
    ids: Optional[list[uuid.UUID]] = None
    issue_boundaries: Optional[list[str]] = None
    issue_types: Optional[list[str]] = None
    scenario_ids: Optional[list[uuid.UUID]] = None

    def construct_filters(self) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []

        self.add_condition_for_property(self.ids, self._id_condition, conditions)

        self.add_condition_for_property(
            self.issue_boundaries, self._tail_node_boundary_condition, conditions,
        )
        self.add_condition_for_property(
            self.issue_types, self._tail_node_issue_type_condition, conditions
        )

        self.add_condition_for_property(
            self.issue_boundaries, self._head_node_boundary_condition, conditions,
        )
        self.add_condition_for_property(
            self.issue_types, self._head_node_issue_type_condition, conditions
        )

        self.add_condition_for_property(self.scenario_ids, self._scenario_id_condition, conditions)

        return conditions

    # Static helper methods to encapsulate condition logic
    @staticmethod
    def _id_condition(id: uuid.UUID) -> ColumnElement[bool]:
        return Edge.id == id

    @staticmethod
    def _scenario_id_condition(scenario_id: uuid.UUID) -> ColumnElement[bool]:
        return Edge.scenario_id == scenario_id

    @staticmethod
    def _tail_node_boundary_condition(issue_boundary: str,) -> ColumnElement[bool]:
        return Edge.tail_node.has(Node.issue.has(Issue.boundary == issue_boundary))

    @staticmethod
    def _tail_node_issue_type_condition(issue_type: str,) -> ColumnElement[bool]:
        return Edge.tail_node.has(Node.issue.has(Issue.type == issue_type))

    @staticmethod
    def _head_node_boundary_condition(issue_boundary: str,) -> ColumnElement[bool]:
        return Edge.head_node.has(Node.issue.has(Issue.boundary == issue_boundary))

    @staticmethod
    def _head_node_issue_type_condition(issue_type: str,) -> ColumnElement[bool]:
        return Edge.head_node.has(Node.issue.has(Issue.type == issue_type))
