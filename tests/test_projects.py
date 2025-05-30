import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.project_dtos import ProjectIncomingDto, ProjectOutgoingDto, ProjectCreateDto
from src.dtos.objective_dtos import ObjectiveViaScenarioDto
from src.dtos.scenario_dtos import ScenarioCreateViaProjectDto

@pytest.mark.asyncio
async def test_get_projects(client: AsyncClient):
    response = await client.get("/projects")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, ProjectOutgoingDto)

@pytest.mark.asyncio
async def test_get_project(client: AsyncClient):
    response = await client.get("/projects/1")
    assert response.status_code == 200

    parse_response_to_dto_test(response, ProjectOutgoingDto)

@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    payload = [ProjectCreateDto(name=str(uuid4()), description=str(uuid4()), scenarios=[]).model_dump()]

    response=await client.post("/projects", json=payload)
    assert response.status_code == 200

    parse_response_to_dtos_test(response, ProjectOutgoingDto)

@pytest.mark.asyncio
async def test_create_project_with_objectives(client: AsyncClient):
    objectives=[ObjectiveViaScenarioDto(name=str(uuid4()), description=str(uuid4())), ObjectiveViaScenarioDto(name=str(uuid4()), description=str(uuid4()))]
    scenarios=[ScenarioCreateViaProjectDto(name=str(uuid4()), project_id=None, objectives=objectives, opportunities=[])]
    payload = [ProjectCreateDto(name=str(uuid4()), description=str(uuid4()),scenarios=scenarios).model_dump()]

    response=await client.post("/projects", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, ProjectOutgoingDto)
    assert response_content[0].scenarios[0].objectives.__len__() == 2

@pytest.mark.asyncio
async def test_update_project(client: AsyncClient):
    new_name=str(uuid4())
    payload=[ProjectIncomingDto(id=3, name=new_name, description="", scenarios=[]).model_dump()]

    response=await client.put("/projects", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, ProjectOutgoingDto)
    assert response_content[0].name==new_name

@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient):

    response=await client.delete("/projects/2")

    assert response.status_code == 200