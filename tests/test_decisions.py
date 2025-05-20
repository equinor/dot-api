import pytest
from httpx import AsyncClient
from tests.utils import parse_response_to_dto, parse_response_to_dtos
from src.dtos.decision_dtos import DecisionIncomingDto, DecisionOutgoingDto


@pytest.mark.asyncio
async def test_get_decisions(client: AsyncClient):
    response = await client.get("/decisions")

    parse_response_to_dtos(response, DecisionOutgoingDto)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_decision(client: AsyncClient):
    response = await client.get("/decisions/20")

    parse_response_to_dto(response, DecisionOutgoingDto)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_decision(client: AsyncClient):
    payload = [DecisionIncomingDto(id=None, options=["yes", "no"]).model_dump()]

    response=await client.post("/decisions", json=payload)

    parse_response_to_dtos(response, DecisionOutgoingDto)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_decision(client: AsyncClient):
    new_options=["yes", "no", "this is testing"]
    payload=[DecisionIncomingDto(id=3, options=new_options).model_dump()]

    response=await client.put("/decisions", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos(response, DecisionOutgoingDto)
    assert response_content[0].options==new_options

@pytest.mark.asyncio
async def test_delete_decision(client: AsyncClient):

    response=await client.delete("/decisions/2")

    assert response.status_code == 200