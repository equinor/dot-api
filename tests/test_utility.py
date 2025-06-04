import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.utility_dtos import UtilityIncomingDto, UtilityOutgoingDto


@pytest.mark.asyncio
async def test_get_utilities(client: AsyncClient):
    response = await client.get("/utilities")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, UtilityOutgoingDto)


@pytest.mark.asyncio
async def test_get_utility(client: AsyncClient):
    response = await client.get("/utilities/20")
    assert response.status_code == 200

    parse_response_to_dto_test(response, UtilityOutgoingDto)

@pytest.mark.asyncio
async def test_update_utility(client: AsyncClient):
    new_values=[100., 5.]
    payload=[UtilityIncomingDto(id=1, issue_id=1, values=new_values).model_dump()]

    response=await client.put("/utilities", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, UtilityOutgoingDto)
    assert response_content[0].values==new_values

@pytest.mark.asyncio
async def test_delete_utility(client: AsyncClient):

    response=await client.delete("/utilities/2")

    assert response.status_code == 200