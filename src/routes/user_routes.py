from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.graph_api import call_ms_graph_api
from src.auth.auth import verify_token
from src.services.user_service import UserService
from src.constants import SwaggerDocumentationConstants
from src.dtos.user_dtos import UserOutgoingDto, UserIncomingDto
from src.dependencies import get_user_service
from src.dependencies import get_db

router = APIRouter(tags=["user"])


@router.get("/user/me")
async def get_me(token: str = Depends(verify_token)) -> UserIncomingDto:
    try:
        return await call_ms_graph_api(token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")


@router.get("/users")
async def get_users(
    user_service: UserService = Depends(get_user_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[UserOutgoingDto]:
    try:
        return await user_service.get_all(session, odata_query=filter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{id}")
async def get_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db),
) -> UserOutgoingDto:
    try:
        result = await user_service.get(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(result) > 0:
        return result[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/users/azure-id/{azure_id}")
async def get_user_by_azure_id(
    azure_id: str,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db),
) -> UserOutgoingDto:
    try:
        result = await user_service.get_by_azure_id(session, azure_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        raise HTTPException(status_code=404)
    else:
        return result
