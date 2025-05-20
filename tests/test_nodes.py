import pytest
from httpx import AsyncClient
from tests.utils import parse_response_to_dto, parse_response_to_dtos
from src.dtos.node_dtos import NodeIncomingDto, NodeOutgoingDto
from src.dtos.decision_dtos import DecisionIncomingDto
from src.dtos.probability_dtos import ProbabilityIncomingDto


@pytest.mark.asyncio
async def test_get_nodes(client: AsyncClient):
    response = await client.get("/nodes")

    parse_response_to_dtos(response, NodeOutgoingDto)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_node(client: AsyncClient):
    response = await client.get("/nodes/20")

    parse_response_to_dto(response, NodeOutgoingDto)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_node(client: AsyncClient):
    decision_options=["testing node create", "yes", "no"]
    payload = [NodeIncomingDto(id=None, graph_id=3, type="decision", decision=DecisionIncomingDto(id=None, options=decision_options), probability=None).model_dump()]

    response=await client.post("/nodes", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos(response, NodeOutgoingDto)
    assert response_content[0].decision is not None and response_content[0].decision.options==decision_options


@pytest.mark.asyncio
async def test_update_node(client: AsyncClient):
    node_id=3
    example_node=parse_response_to_dto(await client.get(f"/nodes/{node_id}"), NodeOutgoingDto)
    if example_node.decision is None or example_node.probability is None:
        raise Exception("example_node.decision should not be None")

    new_options=["yes", "no", "this is testing node update"]
    new_probabilities=[0.1, 0.3, 0.6]
    new_type="probability"
    payload=[NodeIncomingDto(
        id=example_node.id, 
        graph_id=example_node.graph_id, 
        type=new_type,
        decision=DecisionIncomingDto(id=example_node.decision.id, options=new_options),
        probability=ProbabilityIncomingDto(id=example_node.probability.id, probabilities=new_probabilities)
    ).model_dump()]

    response=await client.put("/nodes", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos(response, NodeOutgoingDto)
    assert response_content[0].probability is not None and response_content[0].probability.probabilities==new_probabilities
    assert response_content[0].decision is not None and response_content[0].decision.options==new_options
    assert response_content[0].type==new_type

@pytest.mark.asyncio
async def test_delete_node(client: AsyncClient):

    response=await client.delete("/nodes/2")

    assert response.status_code == 200