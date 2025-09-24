import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.uncertainty_dtos import UncertaintyIncomingDto, UncertaintyOutgoingDto
from src.services.uncertainty_service import UncertaintyService
from src.dependencies import get_uncertainty_service
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_db

router = APIRouter(tags=["uncertainties"])


@router.get("/uncertainties/{id}")
async def get_uncertainty(
    id: uuid.UUID,
    uncertainty_service: UncertaintyService = Depends(get_uncertainty_service),
    session: AsyncSession = Depends(get_db),
) -> UncertaintyOutgoingDto:
    try:
        uncertainties: list[UncertaintyOutgoingDto] = await uncertainty_service.get(
            session, [id]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(uncertainties) > 0:
        return uncertainties[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/uncertainties")
async def get_all_uncertainty(
    uncertainty_service: UncertaintyService = Depends(get_uncertainty_service),
    filter: Optional[str] = Query(
        None, description=SwaggerDocumentationConstants.FILTER_DOC
    ),
    session: AsyncSession = Depends(get_db),
) -> list[UncertaintyOutgoingDto]:
    try:
        uncertainties: list[UncertaintyOutgoingDto] = await uncertainty_service.get_all(
            session, odata_query=filter
        )
        return uncertainties
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/uncertainties/{id}")
async def delete_uncertainty(
    id: uuid.UUID,
    uncertainty_service: UncertaintyService = Depends(get_uncertainty_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await uncertainty_service.delete(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/uncertainties")
async def update_uncertainties(
    dtos: list[UncertaintyIncomingDto],
    uncertainty_service: UncertaintyService = Depends(get_uncertainty_service),
    session: AsyncSession = Depends(get_db),
) -> list[UncertaintyOutgoingDto]:
    try:
        return list(await uncertainty_service.update(session, dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
