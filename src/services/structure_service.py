import uuid
#from tests.test_decision_tree import graph_as_dict
from src.services.decision_tree.utils import Utils
from typing import TYPE_CHECKING, Tuple
from src.services.decision_tree.networkx_wrapper import NetworkXWrapper

from src.services.scenario_service import ScenarioService

class StructureService:
    def __init__(
            self, 
            scenario_service: ScenarioService,
        ):
        self.scenario_service=scenario_service

    async def read_influence_diagram(self, scenario_uuid: uuid.UUID):
        graph_dict = Utils.graph_as_dict(scenario_id=scenario_uuid)
        issues = graph_dict['nodes']
        edges = graph_dict['edges']
        return issues, edges


    async def create_decision_tree(self, scenario_id: uuid.UUID):
        issues, edges = await self.read_influence_diagram(scenario_uuid=scenario_id)

        nx_wrapper = NetworkXWrapper()
        dt = await nx_wrapper.create_decision_tree(scenario_id, issues, edges)
        print(dt.to_json_stream())

    async def find_optimal_decision_pyagrum(self, scenario_id: uuid.UUID):
        issues, edges = await self.scenario_service.get_influence_diagram_data(scenario_id)

   
