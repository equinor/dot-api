import pytest_asyncio
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from src.seed_database import GenerateUuid
from src.dtos.user_dtos import UserIncomingDto
from src.dependencies import get_async_engine
from src.auth.auth import verify_token
from src.services.user_service import get_current_user
from src.main import app

async def mock_verify_token():
    return

app.dependency_overrides[verify_token] = mock_verify_token

async def mock_get_current_user():
    return UserIncomingDto(
        id=None,  
        name="test_user_1",
        azure_id=GenerateUuid.as_string(15)
    )
app.dependency_overrides[get_current_user] = mock_get_current_user

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    host, port = "127.0.0.1", 8080
    await get_async_engine() # populate database
    async with AsyncClient(transport=ASGITransport(app=app, client=(host, port)), base_url="http://test") as client:
        yield client
