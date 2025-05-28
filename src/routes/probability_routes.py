from fastapi import APIRouter, Depends, HTTPException
from src.dtos.probability_dtos import ProbabilityIncomingDto, ProbabilityOutgoingDto
from src.services.probability_service import ProbabilityService
from src.dependencies import get_probability_service

router = APIRouter(tags=["probabilities"])

@router.get("/probabilities/{id}")
async def get_probability(
    id: int,
    probability_service: ProbabilityService = Depends(get_probability_service)
) -> ProbabilityOutgoingDto:
    try:
        probabilities: list[ProbabilityOutgoingDto] = await probability_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(probabilities) > 0:
        return probabilities[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/probabilities")
async def get_all_probability(
    probability_service: ProbabilityService = Depends(get_probability_service)
) -> list[ProbabilityOutgoingDto]:
    try:
        probabilities: list[ProbabilityOutgoingDto] = await probability_service.get_all()
        return probabilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/probabilities/{id}")
async def delete_probability(
    id: int,
    probability_service: ProbabilityService = Depends(get_probability_service)
):
    try:
        await probability_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/probabilities")
async def update_probabilities(
    dtos: list[ProbabilityIncomingDto],
    probability_service: ProbabilityService = Depends(get_probability_service)
)-> list[ProbabilityOutgoingDto]:
    try:
        return list(await probability_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    