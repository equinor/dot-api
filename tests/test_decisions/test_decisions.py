import pytest
from src.dtos.decision_dtos import DecisionIncomingDto
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_post_decision(client: AsyncClient):
    payload = [DecisionIncomingDto(options=[""], id=None).__dict__]
    response = await client.post("/decisions", json=payload)

    assert response.status_code == 200