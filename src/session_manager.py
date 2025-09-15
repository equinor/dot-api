from __future__ import annotations

from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.models.base import Base
from sqlalchemy.pool import AsyncAdaptedQueuePool

from src.config import config
from src.seed_database import seed_database, create_single_project_with_scenario
from src.database import get_connection_string_and_token, build_connection_url, validate_default_scenarios

class SessionManager:
    """Manages asynchronous DB sessions with connection pooling."""

    def __init__(self) -> None:
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    async def init_db(self) -> None:
        """Initialize the database engine and session factory."""
        db_connection_string, token_dict = await get_connection_string_and_token(config.APP_ENV)
        if ":memory:" in db_connection_string:
            self.engine = create_async_engine(
                db_connection_string,
                poolclass=AsyncAdaptedQueuePool,
                pool_size=config.POOL_SIZE,
                max_overflow=config.MAX_OVERFLOW,
                pool_pre_ping=True,
                pool_recycle=config.POOL_RECYCLE,
                echo=config.DEBUG,
            )
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                await seed_database(conn, num_projects=10, num_scenarios=10, num_nodes=50)
                await create_single_project_with_scenario(conn)
        else:
            database_url = build_connection_url(db_connection_string, driver="aioodbc")

            self.engine = create_async_engine(
                database_url,
                poolclass=AsyncAdaptedQueuePool,
                pool_size=config.POOL_SIZE,
                max_overflow=config.MAX_OVERFLOW,
                connect_args={"attrs_before": token_dict},
                pool_pre_ping=True,
                pool_recycle=config.POOL_RECYCLE,
                echo=config.DEBUG,
            )

        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )

        await self.run_start_task()

    async def close(self) -> None:
        """Dispose of the database engine."""
        if self.engine:
            await self.engine.dispose()

    async def run_start_task(self) -> None:
        """Run the database start task."""
        if not self.session_factory:
            raise RuntimeError("Database session factory is not initialized.")

        async for session in self.get_session():
            await validate_default_scenarios(session)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Yield a database session with the correct schema set."""
        if not self.session_factory:
            raise RuntimeError("Database session factory is not initialized.")

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e



# Global instances
sessionmanager = SessionManager()
