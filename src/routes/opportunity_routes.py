import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.opportunity_dtos import (
    OpportunityIncomingDto,
    OpportunityOutgoingDto,
)
from src.services.opportunity_service import OpportunityService
from src.dependencies import get_opportunity_service
from src.services.user_service import get_current_user
from src.dtos.user_dtos import UserIncomingDto
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_db

router = APIRouter(tags=["opportunities"])


@router.post("/opportunities")
async def create_opportunities(
    dtos: list[OpportunityIncomingDto],
    opportunity_service: OpportunityService = Depends(get_opportunity_service),
    current_user: UserIncomingDto = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> list[OpportunityOutgoingDto]:
    try:
        return list(await opportunity_service.create(session, dtos, current_user))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/opportunities/{id}")
async def get_opportunity(
    id: uuid.UUID,
    opportunity_service: OpportunityService = Depends(get_opportunity_service),
    session: AsyncSession = Depends(get_db),
) -> OpportunityOutgoingDto:
    try:
        opportunities: list[OpportunityOutgoingDto] = await opportunity_service.get(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(opportunities) > 0:
        return opportunities[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/opportunities")
async def get_all_opportunity(
    opportunity_service: OpportunityService = Depends(get_opportunity_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[OpportunityOutgoingDto]:
    try:
        opportunities: list[OpportunityOutgoingDto] = await opportunity_service.get_all(
            session, odata_query=filter
        )
        return opportunities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/opportunities/{id}")
async def delete_opportunity(
    id: uuid.UUID,
    opportunity_service: OpportunityService = Depends(get_opportunity_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await opportunity_service.delete(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/opportunities")
async def delete_opportunities(
    ids: list[uuid.UUID] = Query([]),
    opportunity_service: OpportunityService = Depends(get_opportunity_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await opportunity_service.delete(session, ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/opportunities")
async def update_opportunities(
    dtos: list[OpportunityIncomingDto],
    opportunity_service: OpportunityService = Depends(get_opportunity_service),
    current_user: UserIncomingDto = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> list[OpportunityOutgoingDto]:
    try:
        return list(await opportunity_service.update(session, dtos, current_user))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
