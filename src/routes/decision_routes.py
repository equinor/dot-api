from fastapi import APIRouter, Depends, HTTPException
from src.dtos.decision_dtos import DecisionIncomingDto, DecisionOutgoingDto
from src.services.decision_service import DecisionService
from src.dependencies import get_decision_service

router = APIRouter()

@router.post("/decisions/")
async def create_decisions(
    dtos: list[DecisionIncomingDto],
    decision_service: DecisionService = Depends(get_decision_service)
)-> list[DecisionOutgoingDto]:
    try:
        return list(await decision_service.create(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/decisions/{id}")
async def get_decision(
    id: int,
    decision_service: DecisionService = Depends(get_decision_service)
) -> DecisionOutgoingDto:
    try:
        decisions: list[DecisionOutgoingDto] = await decision_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(decisions) > 0:
        return decisions[0]
    else:
        raise HTTPException(status_code=404)
    