from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool

from src.models.base import Base
from src.config import config
from src.seed_database import (
    seed_database,
    create_single_project_with_scenario,
    create_decision_tree_symmetry_DT_from_ID,
    create_decision_tree_symmetry_DT,
)
from src.database import (
    DatabaseConnectionStrings,
    get_connection_string_and_token,
    build_connection_url,
    validate_default_scenarios,
)

# import events to activate them
from src.events import (
    before_flush_event_handler, # type: ignore
    after_flush_event_handler, # type: ignore
    before_commit_event_handler, # type: ignore
    after_commit_event_handler, # type: ignore
)

class SessionManager:
    """Manages asynchronous DB sessions with connection pooling."""

    def __init__(self) -> None:
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    async def _initialize_in_memory_db(self, db_connection_string: str) -> None:
        """Initialize an in-memory database, and populate with test data."""
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
            await create_decision_tree_symmetry_DT_from_ID(conn)
            await create_decision_tree_symmetry_DT(conn)

    async def _initialize_persistent_db(self) -> None:
        """Initialize a persistent database."""
        (
            db_connection_string,
            token_dict,
        ) = await get_connection_string_and_token(config.APP_ENV)
        database_url = build_connection_url(db_connection_string, driver="aioodbc")

        if config.APP_ENV == "local":
            self.engine = create_async_engine(
                database_url,
                poolclass=AsyncAdaptedQueuePool,
                pool_size=config.POOL_SIZE,
                pool_timeout=None,
                max_overflow=config.MAX_OVERFLOW,
                pool_pre_ping=True,
                pool_recycle=config.POOL_RECYCLE,
                echo=config.DEBUG,
            )
        else:
            self.engine = create_async_engine(
                database_url,
                poolclass=AsyncAdaptedQueuePool,
                pool_size=config.POOL_SIZE,
                pool_timeout=None,
                max_overflow=config.MAX_OVERFLOW,
                connect_args={"attrs_before": token_dict},
                pool_pre_ping=True,
                pool_recycle=config.POOL_RECYCLE,
                echo=config.DEBUG,
            )

    def _initialize_session_factory(self) -> None:
        """Initialize the session factory."""
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )

    async def init_db(self) -> None:
        """Initialize the database engine and session factory."""
        db_connection_string = DatabaseConnectionStrings.get_connection_string(config.APP_ENV)

        if ":memory:" in db_connection_string:
            await self._initialize_in_memory_db(db_connection_string)
        else:
            await self._initialize_persistent_db()

        self._initialize_session_factory()

        try:
            await self.run_start_task()
        except Exception:
            # implyes that a different thread is performing the start task
            pass

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
