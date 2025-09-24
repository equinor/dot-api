import pytest
from uuid import uuid4
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.value_metric_dtos import ValueMetricIncomingDto, ValueMetricOutgoingDto
from src.seed_database import GenerateUuid

@pytest.mark.asyncio
async def test_get_value_metrics(client: AsyncClient):
    response = await client.get("/value-metrics")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dtos_test(response, ValueMetricOutgoingDto)

@pytest.mark.asyncio
async def test_get_value_metric(client: AsyncClient):
    response = await client.get(f"/value-metrics/{GenerateUuid.as_string(20)}")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dto_test(response, ValueMetricOutgoingDto)

@pytest.mark.asyncio
async def test_update_value_metric(client: AsyncClient):
    new_name = str(uuid4())
    payload = [ValueMetricIncomingDto(id=GenerateUuid.as_uuid(1), issue_id=GenerateUuid.as_uuid(1), name=new_name).model_dump(mode="json")]

    response = await client.put("/value-metrics", json=payload)
    assert response.status_code == 200, f"Response content: {response.content}"

    response_content = parse_response_to_dtos_test(response, ValueMetricOutgoingDto)
    assert response_content[0].name == new_name

@pytest.mark.asyncio
async def test_delete_value_metric(client: AsyncClient):
    response = await client.delete(f"/value-metrics/{GenerateUuid.as_string(2)}")
    assert response.status_code == 200, f"Response content: {response.content}"
