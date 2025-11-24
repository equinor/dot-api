import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.outcome_dtos import OutcomeIncomingDto, OutcomeOutgoingDto
from src.services.outcome_service import OutcomeService
from src.dependencies import get_outcome_service
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_db

router = APIRouter(tags=["outcomes"])


@router.post("/outcomes")
async def create_outcomes(
    dtos: list[OutcomeIncomingDto],
    outcome_service: OutcomeService = Depends(get_outcome_service),
    session: AsyncSession = Depends(get_db),
) -> list[OutcomeOutgoingDto]:
    try:
        result = list(await outcome_service.create(session, dtos))
        await session.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/outcomes/{id}")
async def get_outcome(
    id: uuid.UUID,
    outcome_service: OutcomeService = Depends(get_outcome_service),
    session: AsyncSession = Depends(get_db),
) -> OutcomeOutgoingDto:
    try:
        outcomes: list[OutcomeOutgoingDto] = await outcome_service.get(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(outcomes) > 0:
        return outcomes[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/outcomes")
async def get_all_outcome(
    outcome_service: OutcomeService = Depends(get_outcome_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[OutcomeOutgoingDto]:
    try:
        outcomes: list[OutcomeOutgoingDto] = await outcome_service.get_all(
            session, odata_query=filter
        )
        return outcomes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/outcomes/{id}")
async def delete_outcome(
    id: uuid.UUID,
    outcome_service: OutcomeService = Depends(get_outcome_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await outcome_service.delete(session, [id])
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/outcomes")
async def delete_outcomes(
    ids: list[uuid.UUID] = Query([]),
    outcome_service: OutcomeService = Depends(get_outcome_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await outcome_service.delete(session, ids)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/outcomes")
async def update_outcomes(
    dtos: list[OutcomeIncomingDto],
    outcome_service: OutcomeService = Depends(get_outcome_service),
    session: AsyncSession = Depends(get_db),
) -> list[OutcomeOutgoingDto]:
    try:
        result = list(await outcome_service.update(session, dtos))
        await session.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
