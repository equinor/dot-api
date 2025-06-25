from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from src.auth.db_auth import DatabaseAuthenticator
from src.services.decision_service import DecisionService
from src.services.project_service import ProjectService
from src.services.objective_service import ObjectiveService
from src.services.opportunity_service import OpportunityService
from src.services.uncertainty_service import UncertaintyService
from src.services.utility_service import UtilityService
from src.services.value_metric_service import ValueMetricService
from src.services.scenario_service import ScenarioService
from src.services.edge_service import EdgeService
from src.services.node_service import NodeService
from src.services.node_style_service import NodeStyleService
from src.services.issue_service import IssueService
from src.database import DatabaseConnectionStrings
from src.models.base import Base
from src.seed_database import seed_database
from src.config import Config
import urllib

config = Config()

db_connection_string = DatabaseConnectionStrings.get_connection_string(config.APP_ENV)
async_engine: AsyncEngine|None = None
async def get_async_engine() -> AsyncEngine:
    global async_engine
    if async_engine is None:
        # create all tables in the in memory database
        if config.APP_ENV == "local":
            async_engine = create_async_engine(db_connection_string, echo=False)
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                await seed_database(conn, num_projects=10, num_scenarios=10, num_nodes=50)
        else:
            database_authenticator = DatabaseAuthenticator()
            await database_authenticator.close()
            token_dict = await database_authenticator.authenticate_db_connection_string()
            params = urllib.parse.quote_plus(db_connection_string.replace('"', ""))
            conn_str = "mssql+aioodbc:///?odbc_connect={}".format(params)
            if token_dict:
                async_engine = create_async_engine(
                    conn_str,
                    echo=False,
                    connect_args={"attrs_before": token_dict}
                )
    return async_engine

async def get_project_service() -> ProjectService:
    return ProjectService(await get_async_engine())

async def get_decision_service() -> DecisionService:
    return DecisionService(await get_async_engine())

async def get_objective_service() -> ObjectiveService:
    return ObjectiveService(await get_async_engine())

async def get_opportunity_service() -> OpportunityService:
    return OpportunityService(await get_async_engine())

async def get_uncertainty_service() -> UncertaintyService:
    return UncertaintyService(await get_async_engine())

async def get_utility_service() -> UtilityService:
    return UtilityService(await get_async_engine())

async def get_value_metric_service() -> ValueMetricService:
    return ValueMetricService(await get_async_engine())

async def get_scenario_service() -> ScenarioService:
    return ScenarioService(await get_async_engine())

async def get_edge_service() -> EdgeService:
    return EdgeService(await get_async_engine())

async def get_node_service() -> NodeService:
    return NodeService(await get_async_engine())

async def get_node_style_service() -> NodeStyleService:
    return NodeStyleService(await get_async_engine())

async def get_issue_service() -> IssueService:
    return IssueService(await get_async_engine())
