from sqlalchemy.orm.strategy_options import _AbstractLoad # type: ignore
from sqlalchemy.orm import selectinload
from src.models import *

class QueryExtensions:
    @staticmethod
    def load_issue_with_relationships() -> list[_AbstractLoad]:
        return [
            selectinload(Issue.decision),
            selectinload(Issue.probability),
            selectinload(Issue.node),
        ]
    
    @staticmethod
    def load_node_with_relationships() -> list[_AbstractLoad]:
        return [
            selectinload(Node.issue).options(
                selectinload(Issue.decision),
                selectinload(Issue.probability),
            )
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