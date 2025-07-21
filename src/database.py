from enum import Enum

from src.config import Config


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