import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.decision_dtos import DecisionIncomingDto, DecisionOutgoingDto
from src.seed_database import GenerateUuid

@pytest.mark.asyncio
async def test_get_decisions(client: AsyncClient):
    response = await client.get("/decisions")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, DecisionOutgoingDto)

@pytest.mark.asyncio
async def test_get_decision(client: AsyncClient):
    response = await client.get(f"/decisions/{GenerateUuid.as_string(20)}")
    assert response.status_code == 200

    parse_response_to_dto_test(response, DecisionOutgoingDto)

@pytest.mark.asyncio
async def test_update_decision(client: AsyncClient):
    new_options = ["yes", "no", "this is testing"]
    payload = [DecisionIncomingDto(id=GenerateUuid.as_uuid(1), issue_id=GenerateUuid.as_uuid(1), alternatives=new_options).model_dump(mode="json")]

    response = await client.put("/decisions", json=payload)
    assert response.status_code == 200

    response_content = parse_response_to_dtos_test(response, DecisionOutgoingDto)
    assert response_content[0].alternatives == new_options

@pytest.mark.asyncio
async def test_delete_decision(client: AsyncClient):
    response = await client.delete(f"/decisions/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200
