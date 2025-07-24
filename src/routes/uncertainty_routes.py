import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.dtos.uncertainty_dtos import UncertaintyIncomingDto, UncertaintyOutgoingDto
from src.services.uncertainty_service import UncertaintyService
from src.dependencies import get_uncertainty_service
from src.constants import SwaggerDocumentationConstants

router = APIRouter(tags=["uncertainties"])

@router.get("/uncertainties/{id}")
async def get_uncertainty(
    id: uuid.UUID,
    uncertainty_service: UncertaintyService = Depends(get_uncertainty_service)
) -> UncertaintyOutgoingDto:
    try:
        uncertainties: list[UncertaintyOutgoingDto] = await uncertainty_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(uncertainties) > 0:
        return uncertainties[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/uncertainties")
async def get_all_uncertainty(
    uncertainty_service: UncertaintyService = Depends(get_uncertainty_service),
    filter: Optional[str]=Query(None, description=SwaggerDocumentationConstants.FILTER_DOC)
) -> list[UncertaintyOutgoingDto]:
    try:
        uncertainties: list[UncertaintyOutgoingDto] = await uncertainty_service.get_all(odata_query=filter)
        return uncertainties
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/uncertainties/{id}")
async def delete_uncertainty(
    id: uuid.UUID,
    uncertainty_service: UncertaintyService = Depends(get_uncertainty_service)
):
    try:
        await uncertainty_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/uncertainties")
async def update_uncertainties(
    dtos: list[UncertaintyIncomingDto],
    uncertainty_service: UncertaintyService = Depends(get_uncertainty_service)
)-> list[UncertaintyOutgoingDto]:
    try:
        return list(await uncertainty_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    