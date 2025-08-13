from sqlalchemy.orm.strategy_options import _AbstractLoad # type: ignore
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from src.models import (
    Issue,
    Node,
    Project,
    Scenario,
    User
)

class QueryExtensions:
    @staticmethod
    def load_issue_with_relationships() -> list[_AbstractLoad]:
        return [
            selectinload(Issue.decision),
            selectinload(Issue.uncertainty),
            selectinload(Issue.utility),
            selectinload(Issue.value_metric),
            selectinload(Issue.node).options(
                selectinload(Node.node_style)
            ),
        ]
    
    @staticmethod
    def load_node_with_relationships() -> list[_AbstractLoad]:
        return [
            selectinload(Node.issue).options(
                selectinload(Issue.decision),
                selectinload(Issue.uncertainty),
                selectinload(Issue.utility),
                selectinload(Issue.value_metric),
            ),
            selectinload(Node.node_style)
        ]

    @staticmethod
    def load_scenario_with_relationships() -> list[_AbstractLoad]:
        return [
            selectinload(Scenario.project),
            selectinload(Scenario.opportunities),
            selectinload(Scenario.objectives),
            selectinload(Scenario.nodes),
            selectinload(Scenario.edges),
            selectinload(Scenario.issues).options(
                *QueryExtensions.load_issue_with_relationships()
            ),
        ]
    
    @staticmethod
    def load_project_with_relationships() -> list[_AbstractLoad]:
        return [
            selectinload(Project.scenarios).options(
                *QueryExtensions.load_scenario_with_relationships()
            )
        ]

    @staticmethod
    def empty_load() -> list[_AbstractLoad]:
        """
        To be used as input for generic repositories when there are no relationships to be loaded.
        """
        return []
    @staticmethod
    def load_user_with_roles() -> list[_AbstractLoad]:
        """
        To be used as input for generic repositories when there are no relationships to be loaded.
        """
        return (
            select(User)
                .options(
                    selectinload(User.project_contributors),
                    selectinload(User.project_owners)
                )
            )