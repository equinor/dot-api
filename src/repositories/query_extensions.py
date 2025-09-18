from sqlalchemy.orm.strategy_options import _AbstractLoad  # type: ignore
from sqlalchemy.orm import joinedload, selectinload
from src.models import (
    Issue,
    Node,
    Edge,
    Project,
    Scenario,
    Decision,
    Uncertainty,
    ProjectRole,
    User,
)

# Use joinedload for single relationships
# Use selectinload for collections
class QueryExtensions:

    @staticmethod
    def load_decision_with_relationships() -> list[_AbstractLoad]:
        return [
            selectinload(Decision.options)
        ]
    
    @staticmethod
    def load_uncertainty_with_relationships() -> list[_AbstractLoad]:
        return [
            selectinload(Uncertainty.outcomes) 
        ]

    @staticmethod
    def load_issue_with_relationships() -> list[_AbstractLoad]:
        return [
            joinedload(Issue.decision).options(
                *QueryExtensions.load_decision_with_relationships()
            ),
            joinedload(Issue.uncertainty).options(
                *QueryExtensions.load_uncertainty_with_relationships()
            ),
            joinedload(Issue.utility),
            joinedload(Issue.value_metric),
            joinedload(Issue.node).options(
                joinedload(Node.node_style) 
            ),
        ]
    
    @staticmethod
    def load_node_with_relationships() -> list[_AbstractLoad]:
        return [
            joinedload(Node.issue).options(
                joinedload(Issue.decision).options(
                    *QueryExtensions.load_decision_with_relationships()
                ),
                joinedload(Issue.uncertainty).options(
                    *QueryExtensions.load_uncertainty_with_relationships()
                ),
                joinedload(Issue.utility),
                joinedload(Issue.value_metric),
            ),
            joinedload(Node.node_style)
        ]

    @staticmethod
    def load_scenario_with_relationships() -> list[_AbstractLoad]:
        return [
            joinedload(Scenario.project),
            selectinload(Scenario.opportunities),
            selectinload(Scenario.objectives),
            selectinload(Scenario.nodes),
            selectinload(Scenario.edges),
            joinedload(Scenario.issues).options(
                *QueryExtensions.load_issue_with_relationships()
            ),
        ]
    
    @staticmethod
    def load_edge_with_relationships() -> list[_AbstractLoad]:
        return [
            joinedload(Edge.tail_node).options(
                *QueryExtensions.load_node_with_relationships()
            ),
            joinedload(Edge.head_node).options(
                *QueryExtensions.load_node_with_relationships()
            ),
        ]
    
    @staticmethod
    def load_project_with_relationships() -> list[_AbstractLoad]:
        return [
            selectinload(Project.scenarios).options(
                *QueryExtensions.load_scenario_with_relationships()
            ),
            selectinload(Project.project_role).options(
                *QueryExtensions.load_role_with_user()
            )
        ]

    @staticmethod
    def empty_load() -> list[_AbstractLoad]:
        """
        To be used as input for generic repositories when there are no relationships to be loaded.
        """
        return []
    
    @staticmethod
    def load_role_with_user() -> list[_AbstractLoad]:
        """
        To be used as input for generic repositories to load user relationships.
        """
        
        return [
            joinedload(ProjectRole.user),
        ]

    @staticmethod
    def load_user_with_roles() -> list[_AbstractLoad]:
        """
        To be used as input for generic repositories to load user relationships.
        """

        return [
            selectinload(User.project_role),
        ]
      