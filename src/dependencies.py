from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from src.services.decision_service import DecisionService
from src.database import connection_strings
from src.models import metadata

# use adapter to change based on environment
connection_string = connection_strings.sql_lite_memory.value

async_engine: AsyncEngine|None = None
async def get_async_engine() -> AsyncEngine:
    global async_engine
    if async_engine is None:
        async_engine = create_async_engine(connection_string, echo=False)

        # create all tables in the in memory database
        if connection_string==connection_strings.sql_lite_memory.value:
            async with async_engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
                
    return async_engine

async def get_decision_service() -> DecisionService:
    return DecisionService(await get_async_engine())