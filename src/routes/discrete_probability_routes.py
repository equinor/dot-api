import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.discrete_probability_dtos import (
    DiscreteProbabilityIncomingDto,
    DiscreteProbabilityOutgoingDto,
)
from src.services.discrete_probability_service import DiscreteProbabilityService
from src.dependencies import get_discrete_probability_service
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_db


router = APIRouter(tags=["discrete_probabilities"])


@router.get("/discrete_probabilities/{id}")
async def get_discrete_probability(
    id: uuid.UUID,
    discrete_probability_service: DiscreteProbabilityService = Depends(get_discrete_probability_service),
    session: AsyncSession = Depends(get_db),
) -> DiscreteProbabilityOutgoingDto:
    try:
        discrete_probabilities: list[DiscreteProbabilityOutgoingDto] = await discrete_probability_service.get(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(discrete_probabilities) > 0:
        return discrete_probabilities[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/discrete_probabilities")
async def get_all_discrete_probability(
    discrete_probability_service: DiscreteProbabilityService = Depends(get_discrete_probability_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[DiscreteProbabilityOutgoingDto]:
    try:
        discrete_probabilities: list[DiscreteProbabilityOutgoingDto] = await discrete_probability_service.get_all(
            session, odata_query=filter
        )
        return discrete_probabilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/discrete_probabilities")
async def update_discrete_probabilities(
    dtos: list[DiscreteProbabilityIncomingDto],
    discrete_probability_service: DiscreteProbabilityService = Depends(get_discrete_probability_service),
    session: AsyncSession = Depends(get_db),
) -> list[DiscreteProbabilityOutgoingDto]:
    try:
        result = list(await discrete_probability_service.update(session, dtos))
        await session.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))