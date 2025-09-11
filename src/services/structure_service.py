import uuid
from tests.test_decision_tree import graph_as_dict
from typing import TYPE_CHECKING, Tuple
from src.services.decision_tree.networkx_wrapper import NetworkXWrapper

if TYPE_CHECKING:
    from src.services.edge_service import EdgeService
    from src.services.issue_service import IssueService
from src.dtos.edge_dtos import EdgeOutgoingDto
from src.dtos.issue_dtos import IssueOutgoingDto

class StructureService:
    def __init__(self, issue_service: 'IssueService', edge_service: 'EdgeService'):
        self.issue_service = issue_service
        self.edge_service = edge_service

    async def read_influence_diagram(self, scenario_uuid: uuid.UUID) -> Tuple[list[IssueOutgoingDto], list[EdgeOutgoingDto]]:
        #issues, edges = SolverService.get_issues_and_edges(scenario_uuid)
        graph_dict = graph_as_dict(scenario_id=scenario_uuid)
        issues = graph_dict['nodes']
        edges = graph_dict['edges']
        return issues, edges


    async def create_decision_tree(self, scenario_id: uuid.UUID):
        issues, edges = await self.read_influence_diagram(scenario_uuid=scenario_id)

        nx_wrapper = NetworkXWrapper()
        dt = await nx_wrapper.create_decision_tree(scenario_id, issues, edges)
        print(dt.to_json_stream())
   
