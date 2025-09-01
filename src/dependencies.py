import urllib.parse
from typing import Optional, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import create_engine, Engine
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
from src.services.outcome_service import OutcomeService
from src.services.option_service import OptionService
from src.services.user_service import UserService
from src.database import DatabaseConnectionStrings
from src.models.base import Base
from src.seed_database import seed_database
from src.config import Config
import urllib

config = Config()
async_engine: AsyncEngine|None = None

async def get_token() -> Optional[dict[Any, Any]]:
    database_authenticator = DatabaseAuthenticator()
    token_dict = await database_authenticator.authenticate_db_connection_string()
    await database_authenticator.close()
    return token_dict

def build_connection_url(db_connection_string: str, driver: str) -> str:
    params = urllib.parse.quote_plus(db_connection_string.replace('"', ""))
    return f"mssql+{driver}:///?odbc_connect={params}"

async def get_async_engine() -> AsyncEngine:
    global async_engine
    db_connection_string = DatabaseConnectionStrings.get_connection_string(config.APP_ENV)
    if async_engine is None:
        # create all tables in the in memory database
        if ":memory:" in db_connection_string:
            async_engine = create_async_engine(
                DatabaseConnectionStrings.get_connection_string(config.APP_ENV), 
                echo=False
            )
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                await seed_database(conn, num_projects=10, num_scenarios=10, num_nodes=50)
        else:
            token_dict = await get_token()
            conn_str = build_connection_url(db_connection_string, driver="aioodbc")
            if config.APP_ENV=="local":
                async_engine = create_async_engine(
                    conn_str,
                    echo=False,
                    pool_size=10,
                    max_overflow=20,
                )

            elif token_dict:
                async_engine = create_async_engine(
                    conn_str,
                    echo=False,
                    connect_args={"attrs_before": token_dict},
                    pool_size=10,
                    max_overflow=20,
                )
    assert async_engine is not None
    return async_engine

async def get_sync_engine(envionment: str = config.APP_ENV) -> Engine:
    sync_engine: Engine|None=None
    db_connection_string = DatabaseConnectionStrings.get_connection_string(envionment)
    token_dict = await get_token()
    conn_str = build_connection_url(db_connection_string, driver="pyodbc")
    if envionment=="local":
        sync_engine = create_engine(
            conn_str,
            echo=False,
        )
    elif token_dict:
        sync_engine = create_engine(
            conn_str,
            echo=False,
            connect_args={"attrs_before": token_dict}
        )
    assert sync_engine is not None
    return sync_engine

async def get_project_service() -> ProjectService:
    return ProjectService(await get_async_engine())


async def get_decision_service() -> DecisionService:
    return DecisionService(await get_async_engine())

async def get_outcome_service() -> OutcomeService:
    return OutcomeService(await get_async_engine())

async def get_option_service() -> OptionService:
    return OptionService(await get_async_engine())

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

async def get_user_service() -> UserService:
    return UserService(await get_async_engine())
