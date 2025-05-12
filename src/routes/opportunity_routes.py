from fastapi import APIRouter, Depends, HTTPException
from src.dtos.opportunity_dtos import OpportunityIncomingDto, OpportunityOutgoingDto
from src.dtos.user_dtos import UserIncomingDto
from src.services.opportunity_service import OpportunityService
from src.dependencies import get_opportunity_service

router = APIRouter(tags=["opportunities"])

@router.post("/opportunities")
async def create_opportunities(
    dtos: list[OpportunityIncomingDto],
    user_dto: UserIncomingDto,
    opportunity_service: OpportunityService = Depends(get_opportunity_service)
)-> list[OpportunityOutgoingDto]:
    try:
        return list(await opportunity_service.create(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/opportunities/{id}")
async def get_opportunity(
    id: int,
    opportunity_service: OpportunityService = Depends(get_opportunity_service)
) -> OpportunityOutgoingDto:
    try:
        opportunities: list[OpportunityOutgoingDto] = await opportunity_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(opportunities) > 0:
        return opportunities[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/opportunities")
async def get_all_opportunity(
    opportunity_service: OpportunityService = Depends(get_opportunity_service)
) -> list[OpportunityOutgoingDto]:
    try:
        opportunities: list[OpportunityOutgoingDto] = await opportunity_service.get_all()
        return opportunities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/opportunities/{id}")
async def delete_opportunity(
    id: int,
    opportunity_service: OpportunityService = Depends(get_opportunity_service)
):
    try:
        await opportunity_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/opportunities")
async def update_opportunities(
    dtos: list[OpportunityIncomingDto],
    user_dto: UserIncomingDto,
    opportunity_service: OpportunityService = Depends(get_opportunity_service)
)-> list[OpportunityOutgoingDto]:
    try:
        return list(await opportunity_service.update(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    