from azure.identity.aio import DefaultAzureCredential
import struct


class DatabaseAuthenticator:
    def __init__(self,):
        self.credential = DefaultAzureCredential()

    async def authenticate_db_connection_string(self) -> dict[int, bytes]:
        """
        Authenticates and retrieves a database connection string token.

        This method uses the Azure credential to obtain an access token for the
        database and then encodes it in UTF-16-LE format. The token is then
        packed into a structure suitable for use with SQL Server connection
        options.

        Returns:
            dict[int, bytes]: A dictionary containing the SQL Server connection
            option for the access token, with the key being the option identifier
            and the value being the packed token structure.
        """
        access_token = await self.credential.get_token("https://database.windows.net/.default")
        token_bytes = access_token.token.encode("UTF-16-LE")
        token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        token_dict = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}
        return token_dict

    async def close(self):
        """
        Closes the credential session.

        This asynchronous method ensures that the credential session is properly closed,
        releasing any resources that were allocated during the authentication process.

        Raises:
            Exception: If there is an issue closing the credential session.
        """
        await self.credential.close()
