import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.option_dtos import OptionIncomingDto, OptionOutgoingDto
from src.services.option_service import OptionService
from src.dependencies import get_option_service
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_db


router = APIRouter(tags=["options"])


@router.post("/options")
async def create_options(
    dtos: list[OptionIncomingDto],
    option_service: OptionService = Depends(get_option_service),
    session: AsyncSession = Depends(get_db),
) -> list[OptionOutgoingDto]:
    try:
        result = list(await option_service.create(session, dtos))
        await session.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/options/{id}")
async def get_option(
    id: uuid.UUID,
    option_service: OptionService = Depends(get_option_service),
    session: AsyncSession = Depends(get_db),
) -> OptionOutgoingDto:
    try:
        options: list[OptionOutgoingDto] = await option_service.get(session, [id])
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
    session: AsyncSession = Depends(get_db),
) -> list[OptionOutgoingDto]:
    try:
        options: list[OptionOutgoingDto] = await option_service.get_all(session, odata_query=filter)
        return options
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/options/{id}")
async def delete_option(
    id: uuid.UUID,
    option_service: OptionService = Depends(get_option_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await option_service.delete(session, [id])
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/options")
async def delete_options(
    ids: list[uuid.UUID] = Query([]),
    option_service: OptionService = Depends(get_option_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await option_service.delete(session, ids)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/options")
async def update_options(
    dtos: list[OptionIncomingDto],
    option_service: OptionService = Depends(get_option_service),
    session: AsyncSession = Depends(get_db),
) -> list[OptionOutgoingDto]:
    try:
        result = list(await option_service.update(session, dtos))
        await session.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
