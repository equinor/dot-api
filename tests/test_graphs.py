import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.graph_dtos import GraphIncomingDto, GraphOutgoingDto


@pytest.mark.asyncio
async def test_get_graphs(client: AsyncClient):
    response = await client.get("/graphs")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, GraphOutgoingDto)

@pytest.mark.asyncio
async def test_get_graph(client: AsyncClient):
    response = await client.get("/graphs/20")
    assert response.status_code == 200
    
    parse_response_to_dto_test(response, GraphOutgoingDto)

@pytest.mark.asyncio
async def test_create_graph(client: AsyncClient):
    payload = [GraphIncomingDto(id=None, project_id=1, name=str(uuid4())).model_dump()]

    response=await client.post("/graphs", json=payload)
    assert response.status_code == 200

    parse_response_to_dtos_test(response, GraphOutgoingDto)

@pytest.mark.asyncio
async def test_update_graph(client: AsyncClient):
    new_name=str(uuid4())
    new_project_id=3
    payload=[GraphIncomingDto(id=3, name=new_name, project_id=new_project_id).model_dump()]

    response=await client.put("/graphs", json=payload)
    assert response.status_code == 200
    response_content=parse_response_to_dtos_test(response, GraphOutgoingDto)
    assert response_content[0].name==new_name and response_content[0].project_id==new_project_id

@pytest.mark.asyncio
async def test_delete_graph(client: AsyncClient):

    response=await client.delete("/graphs/2")

    assert response.status_code == 200