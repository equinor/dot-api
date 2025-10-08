import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.opportunity_dtos import OpportunityIncomingDto, OpportunityOutgoingDto
from src.seed_database import GenerateUuid


@pytest.mark.asyncio
async def test_get_opportunities(client: AsyncClient):
    response = await client.get("/opportunities")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dtos_test(response, OpportunityOutgoingDto)


@pytest.mark.asyncio
async def test_get_opportunity(client: AsyncClient):
    response = await client.get(f"/opportunities/{GenerateUuid.as_string(5)}")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dto_test(response, OpportunityOutgoingDto)


@pytest.mark.asyncio
async def test_create_opportunity(client: AsyncClient):
    payload = [
        OpportunityIncomingDto(
            scenario_id=GenerateUuid.as_uuid(1), description=str(uuid4())
        ).model_dump(mode="json")
    ]

    response = await client.post("/opportunities", json=payload)
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dtos_test(response, OpportunityOutgoingDto)


@pytest.mark.asyncio
async def test_update_opportunity(client: AsyncClient):
    new_description = str(uuid4())
    new_scenario_id = GenerateUuid.as_uuid(3)
    payload = [
        OpportunityIncomingDto(
            id=GenerateUuid.as_uuid(3),
            description=new_description,
            scenario_id=new_scenario_id,
        ).model_dump(mode="json")
    ]

    response = await client.put("/opportunities", json=payload)
    assert response.status_code == 200, f"Response content: {response.content}"

    response_content = parse_response_to_dtos_test(response, OpportunityOutgoingDto)
    assert (
        response_content[0].description == new_description and response_content[0].scenario_id == new_scenario_id
    )


@pytest.mark.asyncio
async def test_delete_opportunity(client: AsyncClient):
    response = await client.delete(f"/opportunities/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200, f"Response content: {response.content}"
