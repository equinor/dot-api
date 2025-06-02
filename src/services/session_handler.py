from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from contextlib import asynccontextmanager

@asynccontextmanager
async def session_handler(engine: AsyncEngine):
    async with AsyncSession(engine, autoflush=True, autocommit=False) as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
