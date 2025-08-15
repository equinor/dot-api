import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.uncertainty_dtos import UncertaintyIncomingDto, UncertaintyOutgoingDto
from src.dtos.outcome_dtos import OutcomeIncomingDto
from src.seed_database import GenerateUuid

@pytest.mark.asyncio
async def test_get_uncertainties(client: AsyncClient):
    response = await client.get("/uncertainties")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, UncertaintyOutgoingDto)

@pytest.mark.asyncio
async def test_get_uncertainty(client: AsyncClient):
    response = await client.get(f"/uncertainties/{GenerateUuid.as_string(20)}")
    assert response.status_code == 200

    parse_response_to_dto_test(response, UncertaintyOutgoingDto)

@pytest.mark.asyncio
async def test_update_uncertainty(client: AsyncClient):
    uncert_id=GenerateUuid.as_uuid(1)
    new_probabilities = [0.2, 0.8]
    new_outcomes = [OutcomeIncomingDto(probability=x, name=str(x), utility=0,uncertainty_id=uncert_id) for x in new_probabilities]    
    payload = [UncertaintyIncomingDto(id=uncert_id, issue_id=GenerateUuid.as_uuid(1), outcomes=new_outcomes).model_dump(mode="json")]

    response = await client.put("/uncertainties", json=payload)
    assert response.status_code == 200

    response_content = parse_response_to_dtos_test(response, UncertaintyOutgoingDto)
    assert [x.probability for x in response_content[0].outcomes] == new_probabilities

@pytest.mark.asyncio
async def test_delete_uncertainty(client: AsyncClient):
    response = await client.delete(f"/uncertainties/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200
