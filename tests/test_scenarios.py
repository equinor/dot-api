import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.scenario_dtos import ScenarioCreateDto, ScenarioIncomingDto, ScenarioOutgoingDto
from src.dtos.objective_dtos import ObjectiveViaScenarioDto, ObjectiveIncomingDto

@pytest.mark.asyncio
async def test_get_scenarios(client: AsyncClient):
    response = await client.get("/scenarios")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, ScenarioOutgoingDto)

@pytest.mark.asyncio
async def test_get_scenario(client: AsyncClient):
    response = await client.get("/scenarios/10")
    assert response.status_code == 200
    
    parse_response_to_dto_test(response, ScenarioOutgoingDto)

@pytest.mark.asyncio
async def test_create_scenario(client: AsyncClient):
    objectives=[ObjectiveViaScenarioDto(name=str(uuid4()), description=str(uuid4())), ObjectiveViaScenarioDto(name=str(uuid4()), description=str(uuid4()))]
    payload = [ScenarioCreateDto(project_id=1, name=str(uuid4()), objectives=objectives, opportunities=[]).model_dump()]

    response=await client.post("/scenarios", json=payload)
    assert response.status_code == 200
    response_content=parse_response_to_dtos_test(response, ScenarioOutgoingDto)
    assert response_content[0].objectives.__len__() == 2

@pytest.mark.asyncio
async def test_update_scenario(client: AsyncClient):
    new_name=str(uuid4())
    new_project_id=3
    objectives=[ObjectiveIncomingDto(id=None, scenario_id=new_project_id, name=str(uuid4()), description=str(uuid4())), ObjectiveIncomingDto(id=None, scenario_id=new_project_id, name=str(uuid4()), description=str(uuid4()))]
    payload=[ScenarioIncomingDto(id=3, name=new_name, project_id=new_project_id, objectives=objectives, opportunities=[]).model_dump()]

    response=await client.put("/scenarios", json=payload)
    assert response.status_code == 200
    response_content=parse_response_to_dtos_test(response, ScenarioOutgoingDto)
    assert response_content[0].name==new_name and response_content[0].project_id==new_project_id and response_content[0].objectives[0].name==objectives[0].name

@pytest.mark.asyncio
async def test_delete_scenario(client: AsyncClient):

    response=await client.delete("/scenarios/2")

    assert response.status_code == 200