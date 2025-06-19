import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.edge_dtos import EdgeIncomingDto, EdgeOutgoingDto
from src.seed_database import GenerateUuid

@pytest.mark.asyncio
async def test_get_edges(client: AsyncClient):
    response = await client.get("/edges")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, EdgeOutgoingDto)

@pytest.mark.asyncio
async def test_get_edge(client: AsyncClient):
    response = await client.get(f"/edges/{GenerateUuid.as_string(20)}")
    assert response.status_code == 200

    parse_response_to_dto_test(response, EdgeOutgoingDto)

@pytest.mark.asyncio
async def test_create_edge(client: AsyncClient):
    payload = [EdgeIncomingDto(tail_id=GenerateUuid.as_uuid(5), head_id=GenerateUuid.as_uuid(4), scenario_id=GenerateUuid.as_uuid(3)).model_dump(mode="json")]

    response = await client.post("/edges", json=payload)
    assert response.status_code == 200

    parse_response_to_dtos_test(response, EdgeOutgoingDto)

@pytest.mark.asyncio
async def test_update_edge(client: AsyncClient):
    new_tail_id = GenerateUuid.as_uuid(2)
    new_head_id = GenerateUuid.as_uuid(8)
    payload = [EdgeIncomingDto(id=GenerateUuid.as_uuid(8), tail_id=new_tail_id, head_id=new_head_id, scenario_id=GenerateUuid.as_uuid(3)).model_dump(mode="json")]

    response = await client.put("/edges", json=payload)
    assert response.status_code == 200

    response_content = parse_response_to_dtos_test(response, EdgeOutgoingDto)
    assert response_content[0].tail_id == new_tail_id and response_content[0].head_id == new_head_id

@pytest.mark.asyncio
async def test_delete_edge(client: AsyncClient):
    response = await client.delete(f"/edges/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200
