import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.utility_dtos import UtilityIncomingDto, UtilityOutgoingDto
from src.seed_database import GenerateUuid


@pytest.mark.asyncio
async def test_get_utilities(client: AsyncClient):
    response = await client.get("/utilities")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dtos_test(response, UtilityOutgoingDto)


@pytest.mark.asyncio
async def test_get_utility(client: AsyncClient):
    response = await client.get(f"/utilities/{GenerateUuid.as_string(20)}")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dto_test(response, UtilityOutgoingDto)


@pytest.mark.asyncio
async def test_update_utility(client: AsyncClient):
    new_values = [100.0, 5.0]
    payload = [
        UtilityIncomingDto(
            id=GenerateUuid.as_uuid(1), issue_id=GenerateUuid.as_uuid(1), values=new_values
        ).model_dump(mode="json")
    ]

    response = await client.put("/utilities", json=payload)
    assert response.status_code == 200, f"Response content: {response.content}"

    response_content = parse_response_to_dtos_test(response, UtilityOutgoingDto)
    assert response_content[0].values == new_values


@pytest.mark.asyncio
async def test_delete_utility(client: AsyncClient):
    response = await client.delete(f"/utilities/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200, f"Response content: {response.content}"
