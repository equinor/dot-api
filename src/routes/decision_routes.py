import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.dtos.decision_dtos import DecisionIncomingDto, DecisionOutgoingDto
from src.services.decision_service import DecisionService
from src.dependencies import get_decision_service

router = APIRouter(tags=["decisions"])

@router.get("/decisions/{id}")
async def get_decision(
    id: uuid.UUID,
    decision_service: DecisionService = Depends(get_decision_service),
) -> DecisionOutgoingDto:
    try:
        decisions: list[DecisionOutgoingDto] = await decision_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(decisions) > 0:
        return decisions[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/decisions")
async def get_all_decision(
    decision_service: DecisionService = Depends(get_decision_service),
    filter: Optional[str] = Query(None),
) -> list[DecisionOutgoingDto]:
    try:
        decisions: list[DecisionOutgoingDto] = await decision_service.get_all(odata_query=filter)
        return decisions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/decisions/{id}")
async def delete_decision(
    id: uuid.UUID,
    decision_service: DecisionService = Depends(get_decision_service)
):
    try:
        await decision_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/decisions")
async def update_decisions(
    dtos: list[DecisionIncomingDto],
    decision_service: DecisionService = Depends(get_decision_service)
)-> list[DecisionOutgoingDto]:
    try:
        return list(await decision_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    