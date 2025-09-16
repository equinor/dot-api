from httpx import AsyncClient
import pytest

from src.dtos.project_roles_dtos import ProjectRoleOutgoingDto
from src.seed_database import GenerateUuid
from tests.utils import parse_response_to_dtos_test


@pytest.mark.asyncio
async def test_get__project_role(client: AsyncClient):
    response = await client.get(f"/project-roles/{GenerateUuid.as_string(1)}")
    assert response.status_code == 200
    parse_response_to_dtos_test(response, ProjectRoleOutgoingDto)

@pytest.mark.asyncio
async def test_get_all_project_role(client: AsyncClient):
    response = await client.get("/project-roles/")
    assert response.status_code == 200
    parse_response_to_dtos_test(response, ProjectRoleOutgoingDto)

@pytest.mark.asyncio
async def test_delete_project_role(client: AsyncClient):
    response = await client.delete(f"/project-roles/{GenerateUuid.as_string(0)}/{GenerateUuid.as_string(0)}")
    assert response.status_code == 200,f"Response content: {response.content}"

@pytest.mark.asyncio
async def test_update_project_role(client: AsyncClient):
    response = await client.delete(f"/project-roles/{GenerateUuid.as_string(2)}/{GenerateUuid.as_string(3)}")
    assert response.status_code == 200