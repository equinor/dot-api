from fastapi import HTTPException
from httpx import AsyncClient
import httpx
import hashlib
from src.dtos.user_dtos import UserIncomingDto
from src.config import config
from async_lru import alru_cache
from src.config import config


def _get_token_hash(token: str) -> str:
    """Create a hash of the token for cache key"""
    return hashlib.sha256(token.encode()).hexdigest()[:16]


@alru_cache(maxsize=config.CACHE_MAX_SIZE, ttl=config.CACHE_DURATION)
async def _call_ms_graph_api_cached(token_hash: str, token: str) -> UserIncomingDto:
    """
    Internal cached function that calls Microsoft Graph API.
    Uses token hash as the cache key for security.
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
            try:
                graph_response: httpx.Response = await client.get(
                    "https://graph.microsoft.com/v1.0/me",
                    headers={"Authorization": f'Bearer {obo_response.json()["access_token"]}'},
                )
                graph = graph_response.json()
                return UserIncomingDto(
                    id=None,  # Assuming the ID is not provided by the Graph API
                    name=graph.get("displayName"),
                    azure_id=graph.get("id"),
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error in call_ms_graph_api: {str(e)}",
                )
        else:
            # If OBO response is not successful, raise an HTTPException or return a default UserIncomingDto
            raise HTTPException(
                status_code=401,
                detail="Failed to obtain access token from Microsoft Graph API",
            )


async def call_ms_graph_api(token: str) -> UserIncomingDto:
    """
    Public interface that calls the cached Microsoft Graph API function.
    """
    token_hash = _get_token_hash(token)
    return await _call_ms_graph_api_cached(token_hash, token)
