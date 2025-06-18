import uuid
from fastapi import APIRouter, Depends, HTTPException
from src.dtos.utility_dtos import UtilityIncomingDto, UtilityOutgoingDto
from src.services.utility_service import UtilityService
from src.dependencies import get_utility_service

router = APIRouter(tags=["utilities"])

@router.get("/utilities/{id}")
async def get_utility(
    id: uuid.UUID,
    utility_service: UtilityService = Depends(get_utility_service)
) -> UtilityOutgoingDto:
    try:
        utilities: list[UtilityOutgoingDto] = await utility_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(utilities) > 0:
        return utilities[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/utilities")
async def get_all_utility(
    utility_service: UtilityService = Depends(get_utility_service)
) -> list[UtilityOutgoingDto]:
    try:
        utilities: list[UtilityOutgoingDto] = await utility_service.get_all()
        return utilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/utilities/{id}")
async def delete_utility(
    id: uuid.UUID,
    utility_service: UtilityService = Depends(get_utility_service)
):
    try:
        await utility_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/utilities")
async def update_utilities(
    dtos: list[UtilityIncomingDto],
    utility_service: UtilityService = Depends(get_utility_service)
)-> list[UtilityOutgoingDto]:
    try:
        return list(await utility_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    