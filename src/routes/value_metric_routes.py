from fastapi import APIRouter, Depends, HTTPException
from src.dtos.value_metric_dtos import ValueMetricIncomingDto, ValueMetricOutgoingDto
from src.services.value_metric_service import ValueMetricService
from src.dependencies import get_value_metric_service

router = APIRouter(tags=["value-metrics"])

@router.get("/value-metrics/{id}")
async def get_value_metric(
    id: int,
    value_metric_service: ValueMetricService = Depends(get_value_metric_service)
) -> ValueMetricOutgoingDto:
    try:
        value_metrics: list[ValueMetricOutgoingDto] = await value_metric_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(value_metrics) > 0:
        return value_metrics[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/value-metrics")
async def get_all_value_metric(
    value_metric_service: ValueMetricService = Depends(get_value_metric_service)
) -> list[ValueMetricOutgoingDto]:
    try:
        value_metrics: list[ValueMetricOutgoingDto] = await value_metric_service.get_all()
        return value_metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/value-metrics/{id}")
async def delete_value_metric(
    id: int,
    value_metric_service: ValueMetricService = Depends(get_value_metric_service)
):
    try:
        await value_metric_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/value-metrics")
async def update_value_metrics(
    dtos: list[ValueMetricIncomingDto],
    value_metric_service: ValueMetricService = Depends(get_value_metric_service)
)-> list[ValueMetricOutgoingDto]:
    try:
        return list(await value_metric_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    