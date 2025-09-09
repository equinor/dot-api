from sqlalchemy.sql import select, asc
from enum import Enum
from src.models import Project, Scenario
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from src.services.session_handler import session_handler
from src.config import Config

from src.auth.db_auth import DatabaseAuthenticator
import urllib.parse
from typing import Optional, Any


config = Config()
class DatabaseConnectionStrings(Enum):
    local = "sqlite+aiosqlite:///:memory:"
    @classmethod
    def get_connection_string(cls, app_env: str) -> str:
        """Retrieve the appropriate connection string based on the application environment."""
        if app_env == "local":
            return cls.local.value
        elif app_env == "dev":
            return config.DATABASE_CONN_DEV
        elif app_env == "test":
            return config.DATABASE_CONN_TEST
        elif app_env == "prod":
            return config.DATABASE_CONN_PROD
        else:
            raise ValueError(f"Unknown environment: {app_env}")
        
async def database_start_task(engine: AsyncEngine):
    async with session_handler(engine) as session:
        await validate_default_scenarios(session)

async def validate_default_scenarios(session: AsyncSession):
    projects = list((await session.scalars(select(Project))).all())

    for project in projects:
        scenarios = list((await session.scalars(
            select(Scenario).where(Scenario.project_id==project.id).order_by(asc(Scenario.created_at))
        )).all())

        if len(scenarios)==0:
            continue
        number_of_default_scenarios=sum([x.is_default for x in scenarios])
        if number_of_default_scenarios == 1:
            continue                
        if number_of_default_scenarios == 0:
            scenarios[0].is_default=True
            await session.flush()
        if number_of_default_scenarios > 1:
            # Keep the first `is_default` as True, set all others to False
            first_default_found = False
            for scenario in scenarios:
                if scenario.is_default and not first_default_found:
                    first_default_found = True
                else:
                    scenario.is_default = False
            await session.flush()

async def get_connection_string_and_token(env: str) -> tuple[str, Optional[dict[Any, Any]]]:
    db_connection_string = DatabaseConnectionStrings.get_connection_string(env)
    database_authenticator = DatabaseAuthenticator()
    token_dict = await database_authenticator.authenticate_db_connection_string()
    await database_authenticator.close()
    return db_connection_string, token_dict

def build_connection_url(db_connection_string: str, driver: str) -> str:
    params = urllib.parse.quote_plus(db_connection_string.replace('"', ""))
    return f"mssql+{driver}:///?odbc_connect={params}"