import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.objective_dtos import ObjectiveIncomingDto, ObjectiveOutgoingDto
from src.seed_database import GenerateUuid

@pytest.mark.asyncio
async def test_get_objectives(client: AsyncClient):
    response = await client.get("/objectives")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, ObjectiveOutgoingDto)

@pytest.mark.asyncio
async def test_get_objective(client: AsyncClient):
    response = await client.get(f"/objectives/{GenerateUuid.as_string(5)}")
    assert response.status_code == 200

    parse_response_to_dto_test(response, ObjectiveOutgoingDto)

@pytest.mark.asyncio
async def test_create_objective(client: AsyncClient):
    payload = [ObjectiveIncomingDto(scenario_id=GenerateUuid.as_uuid(1), name=str(uuid4()), description=str(uuid4())).model_dump(mode="json")]

    response = await client.post("/objectives", json=payload)
    assert response.status_code == 200

    parse_response_to_dtos_test(response, ObjectiveOutgoingDto)

@pytest.mark.asyncio
async def test_update_objective(client: AsyncClient):
    new_name = str(uuid4())
    new_scenario_id = GenerateUuid.as_uuid(3)
    payload = [ObjectiveIncomingDto(id=GenerateUuid.as_uuid(3), description=str(uuid4()), name=new_name, scenario_id=new_scenario_id).model_dump(mode="json")]

    response = await client.put("/objectives", json=payload)
    assert response.status_code == 200

    response_content = parse_response_to_dtos_test(response, ObjectiveOutgoingDto)
    assert response_content[0].name == new_name and response_content[0].scenario_id == new_scenario_id

@pytest.mark.asyncio
async def test_delete_objective(client: AsyncClient):
    response = await client.delete(f"/objectives/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200
