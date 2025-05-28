import pytest_asyncio
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from src.dependencies import get_async_engine

from src.main import app

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    host, port = "127.0.0.1", 8080

    await get_async_engine() # populate database
    async with AsyncClient(transport=ASGITransport(app=app, client=(host, port)), base_url="http://test") as client:
        yield client
