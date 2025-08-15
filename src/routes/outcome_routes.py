import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.dtos.outcome_dtos import OutcomeIncomingDto, OutcomeOutgoingDto
from src.services.outcome_service import OutcomeService
from src.dependencies import get_outcome_service
from src.constants import SwaggerDocumentationConstants

router = APIRouter(tags=["outcomes"])

@router.post("/outcomes")
async def create_outcomes(
    dtos: list[OutcomeIncomingDto],
    outcome_service: OutcomeService = Depends(get_outcome_service),
)-> list[OutcomeOutgoingDto]:
    try:
        return list(await outcome_service.create(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/outcomes/{id}")
async def get_outcome(
    id: uuid.UUID,
    outcome_service: OutcomeService = Depends(get_outcome_service),
) -> OutcomeOutgoingDto:
    try:
        outcomes: list[OutcomeOutgoingDto] = await outcome_service.get([id])
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
) -> list[OutcomeOutgoingDto]:
    try:
        outcomes: list[OutcomeOutgoingDto] = await outcome_service.get_all(odata_query=filter)
        return outcomes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/outcomes/{id}")
async def delete_outcome(
    id: uuid.UUID,
    outcome_service: OutcomeService = Depends(get_outcome_service)
):
    try:
        await outcome_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/outcomes")
async def update_outcomes(
    dtos: list[OutcomeIncomingDto],
    outcome_service: OutcomeService = Depends(get_outcome_service)
)-> list[OutcomeOutgoingDto]:
    try:
        return list(await outcome_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    