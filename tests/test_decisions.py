import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.decision_dtos import DecisionIncomingDto, DecisionOutgoingDto
from src.dtos.option_dtos import OptionIncomingDto
from src.seed_database import GenerateUuid

@pytest.mark.asyncio
async def test_get_decisions(client: AsyncClient):
    response = await client.get("/decisions")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dtos_test(response, DecisionOutgoingDto)

@pytest.mark.asyncio
async def test_get_decision(client: AsyncClient):
    response = await client.get(f"/decisions/{GenerateUuid.as_string(20)}")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dto_test(response, DecisionOutgoingDto)

@pytest.mark.asyncio
async def test_update_decision(client: AsyncClient):
    decision_id = GenerateUuid.as_uuid(1)
    new_alts = ["yes", "no", "this is testing"]
    new_options = [OptionIncomingDto(name=x, utility=0, decision_id=decision_id) for x in new_alts]
    payload = [DecisionIncomingDto(id=decision_id, issue_id=GenerateUuid.as_uuid(1), options=new_options).model_dump(mode="json")]

    response = await client.put("/decisions", json=payload)
    assert response.status_code == 200, f"Response content: {response.content}"

    response_content = parse_response_to_dtos_test(response, DecisionOutgoingDto)
    assert [x.name for x in response_content[0].options] == new_alts

@pytest.mark.asyncio
async def test_delete_decision(client: AsyncClient):
    response = await client.delete(f"/decisions/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200, f"Response content: {response.content}"
