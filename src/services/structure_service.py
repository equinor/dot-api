import uuid
from src.services.scenario_service import ScenarioService
from src.services.decision_tree.decision_tree_creator import DecisionTreeCreator

class StructureService:
    def __init__(self, scenario_service: ScenarioService):
        self.scenario_service=scenario_service

    async def create_decision_tree(self, scenario_id: uuid.UUID):
        issues, edges = await self.scenario_service.get_influence_diagram_data(scenario_id)
        decision_tree_creator = await DecisionTreeCreator.initialize(scenario_id = scenario_id, 
                                            issues = issues, 
                                            edges = edges)
        return await decision_tree_creator.create_decision_tree()


    async def create_decision_tree_json(self, scenario_id: uuid.UUID):
        issues, edges = await self.scenario_service.get_influence_diagram_data(scenario_id)
        decision_tree_creator = await DecisionTreeCreator.initialize(scenario_id = scenario_id, 
                                            issues = issues, 
                                            edges = edges)
        dt = await decision_tree_creator.create_decision_tree()
        return await decision_tree_creator.to_json_stream(dt)   

