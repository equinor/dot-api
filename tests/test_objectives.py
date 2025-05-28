import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.objective_dtos import ObjectiveIncomingDto, ObjectiveOutgoingDto

@pytest.mark.asyncio
async def test_get_objectives(client: AsyncClient):
    response = await client.get("/objectives")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, ObjectiveOutgoingDto)


@pytest.mark.asyncio
async def test_get_objective(client: AsyncClient):
    response = await client.get("/objectives/5")
    assert response.status_code == 200

    parse_response_to_dto_test(response, ObjectiveOutgoingDto)

@pytest.mark.asyncio
async def test_create_objective(client: AsyncClient):
    payload = [ObjectiveIncomingDto(id=None, project_id=1, name=str(uuid4()), description=str(uuid4())).model_dump()]

    response=await client.post("/objectives", json=payload)
    assert response.status_code == 200

    parse_response_to_dtos_test(response, ObjectiveOutgoingDto)

@pytest.mark.asyncio
async def test_update_objective(client: AsyncClient):
    new_name=str(uuid4())
    new_project_id=3
    payload=[ObjectiveIncomingDto(id=3, description=str(uuid4()), name=new_name, project_id=new_project_id).model_dump()]

    response=await client.put("/objectives", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, ObjectiveOutgoingDto)
    assert response_content[0].name==new_name and response_content[0].project_id==new_project_id

@pytest.mark.asyncio
async def test_delete_objective(client: AsyncClient):

    response=await client.delete("/objectives/2")

    assert response.status_code == 200