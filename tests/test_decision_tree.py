import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.seed_database import GenerateUuid

from src.seed_database import GenerateUuid
from src.services.decision_tree.decision_tree_creator import DecisionTreeGraph
from src.services.decision_tree.decision_tree_utils import EdgeUUIDDto
from src.dependencies import get_scenario_service, get_structure_service

@pytest.mark.asyncio
async def test_decision_tree_endpoint(client: AsyncClient):
    scenario_id = GenerateUuid.as_uuid("decision_tree_test_scenario_1")
    response = await client.get(f"/structure/{scenario_id}/DT")
    assert response.status_code == 200, f"Failed to create decision tree: {response.text}"

@pytest.mark.asyncio
async def test_decision_tree():
    scenario_service = await get_scenario_service()
    structure_service = await get_structure_service()
    
    scenario_uuid = GenerateUuid.as_uuid("dt_from_id_scenario")
    dt_from_id = await structure_service.create_decision_tree(scenario_uuid)

    scenario_uuid2 = GenerateUuid.as_uuid("dt_scenario")
    issues, edges = await scenario_service.get_influence_diagram_data(scenario_uuid2)
    root_id = GenerateUuid.as_uuid("dt_uncertainty_S")
    root_issue = next((issue for issue in issues if issue.id == root_id), None)
    decision_tree_graph = DecisionTreeGraph(root=root_issue.id)
    for issue in issues:
        await decision_tree_graph.add_node(issue.id)

    for edge in edges:
        tail_node = [x for x in issues if x.id==edge.tail_node.issue_id][0]
        head_node = [x for x in issues if x.id==edge.head_node.issue_id][0]
        ee = EdgeUUIDDto(tail_node.id, head_node.id, '')
        await decision_tree_graph.add_edge(ee)    

    no_nodes_id = dt_from_id.nx.number_of_nodes()
    no_edges_id = dt_from_id.nx.number_of_edges()

    no_nodes_dt = decision_tree_graph.nx.number_of_nodes()
    no_edges_dt = decision_tree_graph.nx.number_of_edges()

    assert no_edges_id == no_edges_dt
    assert no_nodes_id == no_nodes_dt