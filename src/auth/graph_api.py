from fastapi import HTTPException
from httpx import AsyncClient
import httpx
from src.dtos.user_dtos import (
    UserIncomingDto,
)
from src.config import Config
config = Config()

async def call_ms_graph_api (token: str) -> UserIncomingDto:
    """
    Calls the Microsoft Graph API to get user information.
    """
    async with AsyncClient() as client:
            
        # Use the users access token and fetch a new access token for the Graph API
            obo_response: httpx.Response = await client.post(
                f"https://login.microsoftonline.com/{config.TENANT_ID}/oauth2/v2.0/token",
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                    "client_id": config.CLIENT_ID,
                    "client_secret": config.CLIENT_SECRET,
                    "assertion": token,
                    "scope": "https://graph.microsoft.com/user.read",
                    "requested_token_use": "on_behalf_of",
                },
            )

            if obo_response.is_success:
                
                # Call the graph `/me` endpoint to fetch more information about the current user, using the new token
                graph_response: httpx.Response = await client.get(
                    "https://graph.microsoft.com/v1.0/me",
                    headers={
                        "Authorization": f'Bearer {obo_response.json()["access_token"]}'
                    },
                )
                graph = graph_response.json()
                return UserIncomingDto(
                    id=None,  # Assuming the ID is not provided by the Graph API
                    name=graph.get("displayName"),
                    azure_id=graph.get("id")
                )
            elif not obo_response.is_success:
                raise HTTPException(
                    status_code=obo_response.status_code,
                    detail=f"Graph API error: {obo_response.text}"
                )