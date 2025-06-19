import uuid
from fastapi import APIRouter, Depends, HTTPException
from src.dtos.scenario_dtos import (
    ScenarioIncomingDto, 
    ScenarioOutgoingDto,
    ScenarioCreateDto,
    PopulatedScenarioDto,
)
from src.services.scenario_service import ScenarioService
from src.dependencies import get_scenario_service
from src.services.user_service import get_temp_user

router = APIRouter(tags=["scenarios"])

@router.post("/scenarios")
async def create_scenarios(
    dtos: list[ScenarioCreateDto],
    scenario_service: ScenarioService = Depends(get_scenario_service)
)-> list[ScenarioOutgoingDto]:
    """
    Endpoint for creating Scenarios.
    If Objectives/Opportunities are supplied with the Scenario, then they will be created after the Scenario with the appropriate Id.
    """
    try:
        user_dto=get_temp_user()
        return list(await scenario_service.create(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scenarios/{id}")
async def get_scenario(
    id: uuid.UUID,
    scenario_service: ScenarioService = Depends(get_scenario_service)
) -> ScenarioOutgoingDto:
    try:
        scenarios: list[ScenarioOutgoingDto] = await scenario_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(scenarios) > 0:
        return scenarios[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/scenarios-populated/{id}")
async def get_scenario_populated(
    id: uuid.UUID,
    scenario_service: ScenarioService = Depends(get_scenario_service)
) -> PopulatedScenarioDto:
    try:
        scenarios: list[PopulatedScenarioDto] = await scenario_service.get_populated([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(scenarios) > 0:
        return scenarios[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/scenarios")
async def get_all_scenario(
    scenario_service: ScenarioService = Depends(get_scenario_service)
) -> list[ScenarioOutgoingDto]:
    try:
        scenarios: list[ScenarioOutgoingDto] = await scenario_service.get_all()
        return scenarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/scenarios/{id}")
async def delete_scenario(
    id: uuid.UUID,
    scenario_service: ScenarioService = Depends(get_scenario_service)
):
    try:
        await scenario_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/scenarios")
async def update_scenarios(
    dtos: list[ScenarioIncomingDto],
    scenario_service: ScenarioService = Depends(get_scenario_service)
)-> list[ScenarioOutgoingDto]:
    try:
        user_dto=get_temp_user()
        return list(await scenario_service.update(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    