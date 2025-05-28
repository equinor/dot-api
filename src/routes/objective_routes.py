from fastapi import APIRouter, Depends, HTTPException
from src.dtos.objective_dtos import ObjectiveIncomingDto, ObjectiveOutgoingDto
from src.services.objective_service import ObjectiveService
from src.dependencies import get_objective_service
from src.services.user_service import get_temp_user

router = APIRouter(tags=["objectives"])

@router.post("/objectives")
async def create_objectives(
    dtos: list[ObjectiveIncomingDto],
    objective_service: ObjectiveService = Depends(get_objective_service)
)-> list[ObjectiveOutgoingDto]:
    try:
        user_dto=get_temp_user()
        return list(await objective_service.create(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/objectives/{id}")
async def get_objective(
    id: int,
    objective_service: ObjectiveService = Depends(get_objective_service)
) -> ObjectiveOutgoingDto:
    try:
        objectives: list[ObjectiveOutgoingDto] = await objective_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(objectives) > 0:
        return objectives[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/objectives")
async def get_all_objective(
    objective_service: ObjectiveService = Depends(get_objective_service)
) -> list[ObjectiveOutgoingDto]:
    try:
        objectives: list[ObjectiveOutgoingDto] = await objective_service.get_all()
        return objectives
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/objectives/{id}")
async def delete_objective(
    id: int,
    objective_service: ObjectiveService = Depends(get_objective_service)
):
    try:
        await objective_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/objectives")
async def update_objectives(
    dtos: list[ObjectiveIncomingDto],
    objective_service: ObjectiveService = Depends(get_objective_service)
)-> list[ObjectiveOutgoingDto]:
    try:
        user_dto=get_temp_user()
        return list(await objective_service.update(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    