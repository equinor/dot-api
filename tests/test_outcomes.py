import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.outcome_dtos import OutcomeIncomingDto, OutcomeOutgoingDto
from src.seed_database import GenerateUuid


@pytest.mark.asyncio
async def test_post_outcomes(client: AsyncClient):
    uncertainty_id = GenerateUuid.as_uuid(1)
    outcome_dto=OutcomeIncomingDto(
        name=str(uuid4()),
        probability=0.,
        utility=0.,
        uncertainty_id=uncertainty_id,
    )

    response = await client.post("/outcomes", json=[outcome_dto.model_dump(mode="json")])
    assert response.status_code==200

    response_content=parse_response_to_dtos_test(response, OutcomeOutgoingDto)
    assert response_content[0].probability==outcome_dto.probability

@pytest.mark.asyncio
async def test_get_outcomes(client: AsyncClient):
    response = await client.get("/outcomes")
    print(response)
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dtos_test(response, OutcomeOutgoingDto)

@pytest.mark.asyncio
async def test_get_outcome(client: AsyncClient):
    response = await client.get(f"/outcomes/{GenerateUuid.as_string(20)}")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dto_test(response, OutcomeOutgoingDto)

@pytest.mark.asyncio
async def test_update_outcome(client: AsyncClient):
    outcome_id = GenerateUuid.as_string(1)
    example_outcome = parse_response_to_dto_test(await client.get(f"/outcomes/{outcome_id}"), OutcomeOutgoingDto)
    new_probability=0.5
    payload = [OutcomeIncomingDto(
        id=example_outcome.id,
        name=example_outcome.name,
        uncertainty_id=example_outcome.uncertainty_id,
        probability=new_probability,
        utility=example_outcome.utility
    ).model_dump(mode="json")]

    response = await client.put("/outcomes", json=payload)
    assert response.status_code == 200, f"Response content: {response.content}"

    response_content = parse_response_to_dtos_test(response, OutcomeOutgoingDto)
    assert response_content[0].probability == new_probability

@pytest.mark.asyncio
async def test_delete_outcome(client: AsyncClient):
    response = await client.delete(f"/outcomes/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200, f"Response content: {response.content}"
