import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.uncertainty_dtos import UncertaintyIncomingDto, UncertaintyOutgoingDto


@pytest.mark.asyncio
async def test_get_uncertainties(client: AsyncClient):
    response = await client.get("/uncertainties")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, UncertaintyOutgoingDto)


@pytest.mark.asyncio
async def test_get_uncertainty(client: AsyncClient):
    response = await client.get("/uncertainties/20")
    assert response.status_code == 200

    parse_response_to_dto_test(response, UncertaintyOutgoingDto)

@pytest.mark.asyncio
async def test_update_uncertainty(client: AsyncClient):
    new_probabilities=[0.2, 0.8]
    payload=[UncertaintyIncomingDto(id=1, issue_id=1, probabilities=new_probabilities).model_dump()]

    response=await client.put("/uncertainties", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, UncertaintyOutgoingDto)
    assert response_content[0].probabilities==new_probabilities

@pytest.mark.asyncio
async def test_delete_uncertainty(client: AsyncClient):

    response=await client.delete("/uncertainties/2")

    assert response.status_code == 200