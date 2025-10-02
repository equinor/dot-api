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
from src.services.solver_service import SolverService
from src.services.structure_service import StructureService
from src.database import DatabaseConnectionStrings
from src.models.base import Base
from src.seed_database import (seed_database, create_single_project_with_scenario,
                               create_decision_tree_project_with_scenario,
                               create_decision_tree_symmetry_DT_from_ID,
                               create_decision_tree_symmetry_DT)
from src.config import Config
from src.database import database_start_task
import urllib

config = Config()
async_engine: AsyncEngine|None = None

async def get_connection_string_and_token(env: str) -> tuple[str, Optional[dict[Any, Any]]]:
    db_connection_string = DatabaseConnectionStrings.get_connection_string(env)
    database_authenticator = DatabaseAuthenticator()
    token_dict = await database_authenticator.authenticate_db_connection_string()
    await database_authenticator.close()
    return db_connection_string, token_dict

def build_connection_url(db_connection_string: str, driver: str) -> str:
    params = urllib.parse.quote_plus(db_connection_string.replace('"', ""))
    return f"mssql+{driver}:///?odbc_connect={params}"

async def get_async_engine() -> AsyncEngine:
    global async_engine
    if async_engine is None:
        # create all tables in the in memory database
        if config.APP_ENV == "local":
            async_engine = create_async_engine(
                DatabaseConnectionStrings.get_connection_string(config.APP_ENV), 
                echo=False
            )
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                await seed_database(conn, num_projects=10, num_scenarios=10, num_nodes=50)
                await create_single_project_with_scenario(conn)
                await create_decision_tree_project_with_scenario(conn)
                await create_decision_tree_symmetry_DT_from_ID(conn)
                await create_decision_tree_symmetry_DT(conn)
        else:
            db_connection_string, token_dict = await get_connection_string_and_token(config.APP_ENV)
            conn_str = build_connection_url(db_connection_string, driver="aioodbc")
            if token_dict:
                async_engine = create_async_engine(
                    conn_str,
                    echo=False,
                    connect_args={"attrs_before": token_dict},
                    pool_size=10,
                    max_overflow=20,
                )
                await database_start_task(async_engine)
    assert async_engine is not None
    return async_engine

async def get_sync_engine(envionment: str = config.APP_ENV) -> Engine:
    sync_engine: Engine|None=None
    db_connection_string, token_dict = await get_connection_string_and_token(envionment)
    conn_str = build_connection_url(db_connection_string, driver="pyodbc")
    if token_dict:
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

async def get_solver_service() -> SolverService:
    return SolverService(await get_scenario_service())

async def get_structure_service() -> StructureService:
    return StructureService(await get_scenario_service())