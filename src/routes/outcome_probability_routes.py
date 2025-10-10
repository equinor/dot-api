import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.outcome_probability_dtos import (
    OutcomeProbabilityIncomingDto,
    OutcomeProbabilityOutgoingDto,
)
from src.services.outcome_probability_service import OutcomeProbabilityService
from src.dependencies import get_outcome_probability_service
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_db

router = APIRouter(tags=["outcome_probabilities"])


@router.get("/outcome_probabilities/{id}")
async def get_outcome_probability(
    id: uuid.UUID,
    outcome_probability_service: OutcomeProbabilityService = Depends(get_outcome_probability_service),
    session: AsyncSession = Depends(get_db),
) -> OutcomeProbabilityOutgoingDto:
    try:
        outcome_probabilities: list[OutcomeProbabilityOutgoingDto] = await outcome_probability_service.get(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(outcome_probabilities) > 0:
        return outcome_probabilities[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/outcome_probabilities")
async def get_all_outcome_probability(
    outcome_probability_service: OutcomeProbabilityService = Depends(get_outcome_probability_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[OutcomeProbabilityOutgoingDto]:
    try:
        outcome_probabilities: list[OutcomeProbabilityOutgoingDto] = await outcome_probability_service.get_all(
            session, odata_query=filter
        )
        return outcome_probabilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/outcome_probabilities")
async def create_outcome_probabilities(
    dtos: list[OutcomeProbabilityIncomingDto],
    outcome_probability_service: OutcomeProbabilityService = Depends(get_outcome_probability_service),
    session: AsyncSession = Depends(get_db),
) -> list[OutcomeProbabilityOutgoingDto]:
    try:
        return list(await outcome_probability_service.create(session, dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/outcome_probabilities/{id}")
async def delete_outcome_probability(
    id: uuid.UUID,
    outcome_probability_service: OutcomeProbabilityService = Depends(get_outcome_probability_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await outcome_probability_service.delete(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/outcome_probabilities")
async def delete_outcome_probabilities(
    ids: list[uuid.UUID] = Query([]),
    outcome_probability_service: OutcomeProbabilityService = Depends(get_outcome_probability_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await outcome_probability_service.delete(session, ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/outcome_probabilities")
async def update_outcome_probabilities(
    dtos: list[OutcomeProbabilityIncomingDto],
    outcome_probability_service: OutcomeProbabilityService = Depends(get_outcome_probability_service),
    session: AsyncSession = Depends(get_db),
) -> list[OutcomeProbabilityOutgoingDto]:
    try:
        return list(await outcome_probability_service.update(session, dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))