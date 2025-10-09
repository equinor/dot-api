import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.decision_dtos import DecisionIncomingDto, DecisionOutgoingDto
from src.services.decision_service import DecisionService
from src.dependencies import get_decision_service
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_db

router = APIRouter(tags=["decisions"])


@router.get("/decisions/{id}")
async def get_decision(
    id: uuid.UUID,
    decision_service: DecisionService = Depends(get_decision_service),
    session: AsyncSession = Depends(get_db),
) -> DecisionOutgoingDto:
    try:
        decisions: list[DecisionOutgoingDto] = await decision_service.get(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(decisions) > 0:
        return decisions[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/decisions")
async def get_all_decision(
    decision_service: DecisionService = Depends(get_decision_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[DecisionOutgoingDto]:
    try:
        decisions: list[DecisionOutgoingDto] = await decision_service.get_all(
            session, odata_query=filter
        )
        return decisions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/decisions/{id}")
async def delete_decision(
    id: uuid.UUID,
    decision_service: DecisionService = Depends(get_decision_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await decision_service.delete(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/decisions")
async def delete_decisions(
    ids: list[uuid.UUID] = Query([]),
    decision_service: DecisionService = Depends(get_decision_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await decision_service.delete(session, ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/decisions")
async def update_decisions(
    dtos: list[DecisionIncomingDto],
    decision_service: DecisionService = Depends(get_decision_service),
    session: AsyncSession = Depends(get_db),
) -> list[DecisionOutgoingDto]:
    try:
        return list(await decision_service.update(session, dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
