import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import parse_response_to_dto, parse_response_to_dtos
from src.dtos.project_dtos import ProjectIncomingDto, ProjectOutgoingDto, ProjectCreateDto
from src.dtos.objective_dtos import ObjectiveViaProjectDto


@pytest.mark.asyncio
async def test_get_projects(client: AsyncClient):
    response = await client.get("/projects")

    parse_response_to_dtos(response, ProjectOutgoingDto)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_project(client: AsyncClient):
    response = await client.get("/projects/1")

    parse_response_to_dto(response, ProjectOutgoingDto)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    payload = [ProjectCreateDto(name=str(uuid4()), description=str(uuid4()), Objectives=[], Opportunities=[]).model_dump()]

    response=await client.post("/projects", json=payload)

    parse_response_to_dtos(response, ProjectOutgoingDto)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_project_with_objectives(client: AsyncClient):
    objectives=[ObjectiveViaProjectDto(name=str(uuid4()), description=str(uuid4())), ObjectiveViaProjectDto(name=str(uuid4()), description=str(uuid4()))]
    payload = [ProjectCreateDto(name=str(uuid4()), description=str(uuid4()), Objectives=objectives, Opportunities=[]).model_dump()]

    response=await client.post("/projects", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos(response, ProjectOutgoingDto)
    assert response_content[0].Objectives.__len__() == 2

@pytest.mark.asyncio
async def test_update_project(client: AsyncClient):
    new_name=str(uuid4())
    payload=[ProjectIncomingDto(id=3, name=new_name, description="", Objectives=[], Opportunities=[]).model_dump()]

    response=await client.put("/projects", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos(response, ProjectOutgoingDto)
    assert response_content[0].name==new_name

@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient):

    response=await client.delete("/projects/2")

    assert response.status_code == 200