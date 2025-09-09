import uuid
import pytest_asyncio
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from src.dtos.user_dtos import UserIncomingDto
from asgi_lifespan import LifespanManager
from src.auth.auth import verify_token
from src.services.user_service import get_current_user
from src.main import app

async def mock_verify_token():
    return

app.dependency_overrides[verify_token] = mock_verify_token

async def mock_get_current_user():
    return UserIncomingDto(
        id=None,  # Assuming the ID is not needed for the test
        name="test_user_1",
        azure_id=str(uuid.uuid4())  
    )
app.dependency_overrides[get_current_user] = mock_get_current_user

@pytest_asyncio.fixture(scope="session")
async def lifespan_manager() -> AsyncGenerator[None, None]:
    """
    Fixture to manage the app's lifespan (startup and shutdown) for the entire test session.
    """
    async with LifespanManager(app, startup_timeout=600, shutdown_timeout=600):
        yield 

@pytest_asyncio.fixture
async def client(lifespan_manager) -> AsyncGenerator[AsyncClient, None]:
    host, port = "127.0.0.1", 8080
    async with AsyncClient(transport=ASGITransport(app=app, client=(host, port)), base_url="http://test") as client:
        yield client
