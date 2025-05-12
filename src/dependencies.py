from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from src.services.decision_service import DecisionService
from src.services.project_service import ProjectService
from src.services.objective_service import ObjectiveService
from src.services.opportunity_service import OpportunityService
from src.services.probability_service import ProbabilityService
from src.services.graph_service import GraphService
from src.services.edge_service import EdgeService
from src.services.node_service import NodeService
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

async def get_project_service() -> ProjectService:
    return ProjectService(await get_async_engine())

async def get_decision_service() -> DecisionService:
    return DecisionService(await get_async_engine())

async def get_objective_service() -> ObjectiveService:
    return ObjectiveService(await get_async_engine())

async def get_opportunity_service() -> OpportunityService:
    return OpportunityService(await get_async_engine())

async def get_probability_service() -> ProbabilityService:
    return ProbabilityService(await get_async_engine())

async def get_graph_service() -> GraphService:
    return GraphService(await get_async_engine())

async def get_edge_service() -> EdgeService:
    return EdgeService(await get_async_engine())

async def get_node_service() -> NodeService:
    return NodeService(await get_async_engine())
