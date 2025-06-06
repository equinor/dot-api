import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.opportunity_dtos import OpportunityIncomingDto, OpportunityOutgoingDto


@pytest.mark.asyncio
async def test_get_opportunities(client: AsyncClient):
    response = await client.get("/opportunities")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, OpportunityOutgoingDto)

@pytest.mark.asyncio
async def test_get_opportunity(client: AsyncClient):
    response = await client.get("/opportunities/5")
    assert response.status_code == 200

    parse_response_to_dto_test(response, OpportunityOutgoingDto)

@pytest.mark.asyncio
async def test_create_opportunity(client: AsyncClient):
    payload = [OpportunityIncomingDto(id=None, scenario_id=1, name=str(uuid4()), description=str(uuid4())).model_dump()]

    response=await client.post("/opportunities", json=payload)
    assert response.status_code == 200

    parse_response_to_dtos_test(response, OpportunityOutgoingDto)

@pytest.mark.asyncio
async def test_update_opportunity(client: AsyncClient):
    new_name=str(uuid4())
    new_project_id=3
    payload=[OpportunityIncomingDto(id=3, description=str(uuid4()), name=new_name, scenario_id=new_project_id).model_dump()]

    response=await client.put("/opportunities", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, OpportunityOutgoingDto)
    assert response_content[0].name==new_name and response_content[0].scenario_id==new_project_id

@pytest.mark.asyncio
async def test_delete_opportunity(client: AsyncClient):

    response=await client.delete("/opportunities/2")

    assert response.status_code == 200