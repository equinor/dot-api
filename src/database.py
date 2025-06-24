from enum import Enum
from urllib import parse

class connection_strings(Enum):
    sql_lite_memory="sqlite+aiosqlite:///:memory:"
    ODBC_Msi_dev="mssql+aioodbc://decision-optimization-sqlserver-dev.database.windows.net:1433/decision-optimization-sqldb-dev?uid=decision-optimization-identity-dev&driver=ODBC+Driver+18+for+SQL+Server&authentication=ActiveDirectoryMsi&connectionTimeout=60"
