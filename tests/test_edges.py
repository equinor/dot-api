import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.edge_dtos import EdgeIncomingDto, EdgeOutgoingDto


@pytest.mark.asyncio
async def test_get_edges(client: AsyncClient):
    response = await client.get("/edges")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, EdgeOutgoingDto)

@pytest.mark.asyncio
async def test_get_edge(client: AsyncClient):
    response = await client.get("/edges/20")
    assert response.status_code == 200

    parse_response_to_dto_test(response, EdgeOutgoingDto)

@pytest.mark.asyncio
async def test_create_edge(client: AsyncClient):
    payload = [EdgeIncomingDto(id=None, lower_id=5, higher_id=4, graph_id=3).model_dump()]

    response=await client.post("/edges", json=payload)
    assert response.status_code == 200

    parse_response_to_dtos_test(response, EdgeOutgoingDto)


@pytest.mark.asyncio
async def test_update_edge(client: AsyncClient):
    new_lower_id=2
    new_higher_id=8
    payload=[EdgeIncomingDto(id=8, lower_id=new_lower_id, higher_id=new_higher_id, graph_id=3).model_dump()]

    response=await client.put("/edges", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, EdgeOutgoingDto)
    assert response_content[0].lower_id==new_lower_id and response_content[0].higher_id==new_higher_id

@pytest.mark.asyncio
async def test_delete_edge(client: AsyncClient):

    response=await client.delete("/edges/2")

    assert response.status_code == 200