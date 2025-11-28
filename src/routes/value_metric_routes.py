import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.value_metric_dtos import (
    ValueMetricIncomingDto,
    ValueMetricOutgoingDto,
)
from src.services.value_metric_service import ValueMetricService
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_value_metric_service
from src.dependencies import get_db


router = APIRouter(tags=["value-metrics"])


@router.get("/value-metrics/{id}")
async def get_value_metric(
    id: uuid.UUID,
    value_metric_service: ValueMetricService = Depends(get_value_metric_service),
    session: AsyncSession = Depends(get_db),
) -> ValueMetricOutgoingDto:
    try:
        value_metrics: list[ValueMetricOutgoingDto] = await value_metric_service.get(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(value_metrics) > 0:
        return value_metrics[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/value-metrics")
async def get_all_value_metric(
    value_metric_service: ValueMetricService = Depends(get_value_metric_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[ValueMetricOutgoingDto]:
    try:
        value_metrics: list[ValueMetricOutgoingDto] = await value_metric_service.get_all(
            session, odata_query=filter
        )
        return value_metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/value-metrics/{id}")
async def delete_value_metric(
    id: uuid.UUID,
    value_metric_service: ValueMetricService = Depends(get_value_metric_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await value_metric_service.delete(session, [id])
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/value-metrics")
async def delete_value_metrics(
    ids: list[uuid.UUID] = Query([]),
    value_metric_service: ValueMetricService = Depends(get_value_metric_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await value_metric_service.delete(session, ids)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/value-metrics")
async def update_value_metrics(
    dtos: list[ValueMetricIncomingDto],
    value_metric_service: ValueMetricService = Depends(get_value_metric_service),
    session: AsyncSession = Depends(get_db),
) -> list[ValueMetricOutgoingDto]:
    try:
        result = list(await value_metric_service.update(session, dtos))
        await session.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
