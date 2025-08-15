import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.dtos.option_dtos import OptionIncomingDto, OptionOutgoingDto
from src.services.option_service import OptionService
from src.dependencies import get_option_service
from src.constants import SwaggerDocumentationConstants

router = APIRouter(tags=["options"])

@router.post("/options")
async def create_options(
    dtos: list[OptionIncomingDto],
    option_service: OptionService = Depends(get_option_service),
)-> list[OptionOutgoingDto]:
    try:
        return list(await option_service.create(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options/{id}")
async def get_option(
    id: uuid.UUID,
    option_service: OptionService = Depends(get_option_service),
) -> OptionOutgoingDto:
    try:
        options: list[OptionOutgoingDto] = await option_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(options) > 0:
        return options[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/options")
async def get_all_option(
    option_service: OptionService = Depends(get_option_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
) -> list[OptionOutgoingDto]:
    try:
        options: list[OptionOutgoingDto] = await option_service.get_all(odata_query=filter)
        return options
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/options/{id}")
async def delete_option(
    id: uuid.UUID,
    option_service: OptionService = Depends(get_option_service)
):
    try:
        await option_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/options")
async def update_options(
    dtos: list[OptionIncomingDto],
    option_service: OptionService = Depends(get_option_service)
)-> list[OptionOutgoingDto]:
    try:
        return list(await option_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    