import pytest_asyncio
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from src.seed_database import GenerateUuid
from src.dtos.user_dtos import UserIncomingDto
from asgi_lifespan import LifespanManager
from src.auth.auth import verify_token
from src.services.user_service import get_current_user
from src.main import app, config

def check_test_environment():
    if config.APP_ENV != "local":
        raise Exception("Tests must be ran in local environment")
    if ":memory:" not in config.DATABASE_CONN_LOCAL:
        raise Exception("Tests must be ran using an in memory database")

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

@pytest_asyncio.fixture(scope="session")
async def lifespan_manager() -> AsyncGenerator[None, None]:
    """
    Fixture to manage the app's lifespan (startup and shutdown) for the entire test session.
    """
    check_test_environment()
    async with LifespanManager(app, startup_timeout=600, shutdown_timeout=600):
        yield 

@pytest_asyncio.fixture
async def client(lifespan_manager) -> AsyncGenerator[AsyncClient, None]:
    check_test_environment()
    host, port = "127.0.0.1", 8080
    async with AsyncClient(transport=ASGITransport(app=app, client=(host, port)), base_url="http://test") as client:
        yield client
