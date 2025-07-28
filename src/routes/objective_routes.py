import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.dtos.objective_dtos import ObjectiveIncomingDto, ObjectiveOutgoingDto
from src.services.objective_service import ObjectiveService
from src.dependencies import get_objective_service
from src.services.user_service import get_current_user
from src.dtos.user_dtos import UserIncomingDto
from src.constants import SwaggerDocumentationConstants

router = APIRouter(tags=["objectives"])

@router.post("/objectives")
async def create_objectives(
    dtos: list[ObjectiveIncomingDto],
    objective_service: ObjectiveService = Depends(get_objective_service),
    current_user: UserIncomingDto = Depends(get_current_user)
)-> list[ObjectiveOutgoingDto]:
    try:
        return list(await objective_service.create(dtos, current_user))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/objectives/{id}")
async def get_objective(
    id: uuid.UUID,
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
    objective_service: ObjectiveService = Depends(get_objective_service),
    filter: Optional[str]=Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
) -> list[ObjectiveOutgoingDto]:
    try:
        objectives: list[ObjectiveOutgoingDto] = await objective_service.get_all(odata_query=filter)
        return objectives
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/objectives/{id}")
async def delete_objective(
    id: uuid.UUID,
    objective_service: ObjectiveService = Depends(get_objective_service)
):
    try:
        await objective_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/objectives")
async def update_objectives(
    dtos: list[ObjectiveIncomingDto],
    objective_service: ObjectiveService = Depends(get_objective_service),
    current_user: UserIncomingDto = Depends(get_current_user)
)-> list[ObjectiveOutgoingDto]:
    try:
        return list(await objective_service.update(dtos, current_user))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    