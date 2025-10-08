import uuid
from typing import Optional
from src.services.scenario_service import ScenarioService
from src.dtos.decision_tree_dtos import DecisionTreeDTO
from src.services.decision_tree.decision_tree_creator import DecisionTreeCreator, DecisionTreeGraph
from src.session_manager import sessionmanager

class StructureService:
    def __init__(self, scenario_service: ScenarioService):
        self.scenario_service=scenario_service

    async def create_decision_tree(self, scenario_id: uuid.UUID) -> DecisionTreeGraph :
        issues = []
        edges = []
        async for session in sessionmanager.get_session():
            (
                issues,
                edges,
            ) = await self.scenario_service.get_influence_diagram_data(session, scenario_id)
        decision_tree_creator = await DecisionTreeCreator.initialize(scenario_id = scenario_id,
                                            nodes = issues,
                                            edges = edges)
        return await decision_tree_creator.create_decision_tree()


    async def create_decision_tree_dtos(self, scenario_id: uuid.UUID) -> Optional[DecisionTreeDTO]:
        issues = []
        edges = []
        async for session in sessionmanager.get_session():
            (
                issues,
                edges,
            ) = await self.scenario_service.get_influence_diagram_data(session, scenario_id)
        decision_tree_creator = await DecisionTreeCreator.initialize(scenario_id = scenario_id,
                                            nodes = issues,
                                            edges = edges)
        dt = await decision_tree_creator.create_decision_tree()
        return await decision_tree_creator.to_issue_dtos(dt)
