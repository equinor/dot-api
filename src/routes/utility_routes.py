import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.utility_dtos import UtilityIncomingDto, UtilityOutgoingDto
from src.services.utility_service import UtilityService
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_utility_service
from src.dependencies import get_db
from src.utils.session_commit import commit_if_changed_async

router = APIRouter(tags=["utilities"])


@router.get("/utilities/{id}")
async def get_utility(
    id: uuid.UUID,
    utility_service: UtilityService = Depends(get_utility_service),
    session: AsyncSession = Depends(get_db),
) -> UtilityOutgoingDto:
    try:
        utilities: list[UtilityOutgoingDto] = await utility_service.get(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(utilities) > 0:
        return utilities[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/utilities")
async def get_all_utility(
    utility_service: UtilityService = Depends(get_utility_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[UtilityOutgoingDto]:
    try:
        utilities: list[UtilityOutgoingDto] = await utility_service.get_all(
            session, odata_query=filter
        )
        return utilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/utilities/{id}")
async def delete_utility(
    id: uuid.UUID,
    utility_service: UtilityService = Depends(get_utility_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await utility_service.delete(session, [id])
        await commit_if_changed_async(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/utilities")
async def delete_utilities(
    ids: list[uuid.UUID] = Query([]),
    utility_service: UtilityService = Depends(get_utility_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await utility_service.delete(session, ids)
        await commit_if_changed_async(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/utilities")
async def update_utilities(
    dtos: list[UtilityIncomingDto],
    utility_service: UtilityService = Depends(get_utility_service),
    session: AsyncSession = Depends(get_db),
) -> list[UtilityOutgoingDto]:
    try:
        result = list(await utility_service.update(session, dtos))
        await commit_if_changed_async(session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
