import uuid
from typing import Optional
from sqlalchemy.sql import and_, or_, true, select, Select
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore
from src.models import Issue, Scenario, Node
from sqlalchemy.orm import Mapped, Query
from src.repositories.query_extensions import QueryExtensions


class WhereClauseBuilder:

    @staticmethod
    def scenario_conditions(project_id: Optional[uuid.UUID] = None) -> list[_ColumnExpressionArgument[bool]]:
        conditions: list[_ColumnExpressionArgument[bool]] = []

        if project_id:
            conditions.append(Scenario.project_id == project_id)

        return conditions

    @staticmethod
    def issue_conditions(
        scenario_id: Optional[uuid.UUID] = None,
        project_id: Optional[uuid.UUID] = None
    ) -> list[_ColumnExpressionArgument[bool]]:
        # Start with parent conditions (scenario conditions)
        conditions = WhereClauseBuilder.scenario_conditions(project_id)

        if scenario_id:
            conditions.append(Issue.scenario_id == scenario_id)

        return conditions

    @staticmethod
    def node_conditions(
        scenario_id: Optional[uuid.UUID] = None,
        project_id: Optional[uuid.UUID] = None,
        issue_id: Optional[uuid.UUID] = None
    ) -> list[_ColumnExpressionArgument[bool]]:
        # Start with parent conditions (issue conditions)
        conditions = WhereClauseBuilder.issue_conditions(scenario_id, project_id)

        if issue_id:
            conditions.append(Node.issue_id == issue_id)

        return conditions