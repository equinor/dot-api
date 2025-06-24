from sqlalchemy.types import TypeDecorator, TypeEngine
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import UUID
from sqlalchemy.engine import Dialect
import uuid
from typing import Optional


class GUID(TypeDecorator[uuid.UUID]):
    """
    Platform-independent GUID/UUID type.

    - For MSSQL, it uses UNIQUEIDENTIFIER.
    - For SQLite, it uses UUID.
    """
    impl = UNIQUEIDENTIFIER  # Default implementation for MSSQL
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[uuid.UUID]:
        """
        Determines the underlying database type to use based on the dialect.
        """
        if dialect.name == "mssql":
            return dialect.type_descriptor(UNIQUEIDENTIFIER(as_uuid=True))
        elif dialect.name == "sqlite":
            return dialect.type_descriptor(UUID(as_uuid=True))
        else:
            raise NotImplementedError(f"GUID type is not implemented for dialect: {dialect.name}")

    def process_bind_param(self, value: Optional[uuid.UUID], dialect: Dialect) -> Optional[uuid.UUID]:
        """
        Converts a Python UUID object into a format suitable for the database.
        """
        if value is None:
            return None
        return value

    def process_result_value(self, value: Optional[uuid.UUID], dialect: Dialect) -> Optional[uuid.UUID]:
        """
        Converts a database value back into a Python UUID object.
        """
        if value is None:
            return None
        return value
