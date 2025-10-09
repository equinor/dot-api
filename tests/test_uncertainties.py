import pytest
import uuid
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.uncertainty_dtos import UncertaintyIncomingDto, UncertaintyOutgoingDto
from src.dtos.outcome_dtos import OutcomeIncomingDto
from src.dtos.outcome_probability_dtos import OutcomeProbabilityIncomingDto
from src.seed_database import GenerateUuid


@pytest.mark.asyncio
async def test_get_uncertainties(client: AsyncClient):
    response = await client.get("/uncertainties")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dtos_test(response, UncertaintyOutgoingDto)


@pytest.mark.asyncio
async def test_get_uncertainty(client: AsyncClient):
    response = await client.get(f"/uncertainties/{GenerateUuid.as_string(20)}")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dto_test(response, UncertaintyOutgoingDto)


@pytest.mark.asyncio
async def test_update_uncertainty(client: AsyncClient):
    uncert_id = GenerateUuid.as_uuid(1)
    new_outcome_id = uuid.uuid4()
    new_probability = 0.2
    new_probabilities = [OutcomeProbabilityIncomingDto(
        id = uuid.uuid4(),
        uncertainty_id=uncert_id,
        probability=new_probability,
        child_outcome_id= new_outcome_id,
        parent_option_ids=[],
        parent_outcome_ids=[],
    )]
    new_outcomes = [
        OutcomeIncomingDto(id=new_outcome_id, name=str(new_outcome_id), utility=0, uncertainty_id=uncert_id, )
    ]
    payload = [
        UncertaintyIncomingDto(
            id=uncert_id, issue_id=GenerateUuid.as_uuid(1), outcomes=new_outcomes,
            outcome_probabilities=new_probabilities
        ).model_dump(mode="json")
    ]

    response = await client.put("/uncertainties", json=payload)
    assert response.status_code == 200, f"Response content: {response.content}"

    response_content = parse_response_to_dtos_test(response, UncertaintyOutgoingDto)
    assert response_content[0].outcome_probabilities[0].probability == new_probability


@pytest.mark.asyncio
async def test_delete_uncertainty(client: AsyncClient):
    response = await client.delete(f"/uncertainties/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200, f"Response content: {response.content}"
