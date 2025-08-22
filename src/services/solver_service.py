import uuid
from src.constants import Boundary, Type
from src.services.pyagrum_solver import PyagrumSolver
from src.services.issue_service import IssueService
from src.services.edge_service import EdgeService
from src.models.filters.edge_filter import EdgeFilter
from src.models.filters.issues_filter import IssueFilter
from src.dtos.issue_dtos import IssueOutgoingDto
from src.dtos.edge_dtos import EdgeOutgoingDto

class SolverService:
    def __init__(
            self, 
            issue_service: IssueService,
            edge_service: EdgeService,
        ):
        self.issue_service=issue_service
        self.edge_service=edge_service

    async def get_issues_and_edges(self, scenario_id: uuid.UUID) -> tuple[list[IssueOutgoingDto], list[EdgeOutgoingDto]]:
        issue_filter = IssueFilter(
            scenario_ids=[scenario_id],
            boundaries=[Boundary.ON.value, Boundary.IN.value],
            types=[Type.DECISION.value, Type.UNCERTAINTY.value]
        )
        edge_filter = EdgeFilter(
            scenario_ids=[scenario_id],
            issue_boundaries=[Boundary.ON.value, Boundary.IN.value],
            issue_types=[Type.DECISION.value, Type.UNCERTAINTY.value]
        )

        issues = await self.issue_service.get_all(filter=issue_filter)
        edges = await self.edge_service.get_all(filter=edge_filter)

        return issues, edges
    
    async def find_optimal_decision_pyagrum(self, scenario_id: uuid.UUID):
        issues, edges = await self.get_issues_and_edges(scenario_id)

        solution = PyagrumSolver().find_optimal_decisions(issues=issues, edges=edges)

        return solution
