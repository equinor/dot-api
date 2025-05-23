import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.probability_dtos import ProbabilityIncomingDto, ProbabilityOutgoingDto


@pytest.mark.asyncio
async def test_get_probabilities(client: AsyncClient):
    response = await client.get("/probabilities")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, ProbabilityOutgoingDto)


@pytest.mark.asyncio
async def test_get_probability(client: AsyncClient):
    response = await client.get("/probabilities/20")
    assert response.status_code == 200

    parse_response_to_dto_test(response, ProbabilityOutgoingDto)

@pytest.mark.asyncio
async def test_create_probability(client: AsyncClient):
    payload = [ProbabilityIncomingDto(id=None, probabilities=[0.7, 0.3]).model_dump()]

    response=await client.post("/probabilities", json=payload)
    assert response.status_code == 200

    parse_response_to_dtos_test(response, ProbabilityOutgoingDto)

@pytest.mark.asyncio
async def test_update_probability(client: AsyncClient):
    new_probabilities=[0.2, 0.8]
    payload=[ProbabilityIncomingDto(id=3, probabilities=new_probabilities).model_dump()]

    response=await client.put("/probabilities", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, ProbabilityOutgoingDto)
    assert response_content[0].probabilities==new_probabilities

@pytest.mark.asyncio
async def test_delete_probability(client: AsyncClient):

    response=await client.delete("/probabilities/2")

    assert response.status_code == 200