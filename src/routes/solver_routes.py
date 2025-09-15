import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.solver_service import SolverService
from src.dependencies import get_solver_service
from src.services.user_service import get_current_user
from src.dtos.user_dtos import UserIncomingDto
from src.dependencies import get_db

router = APIRouter(tags=["solvers"])

@router.get("/solvers/scenario/{scenario_id}")
async def get_optimal_decisions_for_scenario(
    scenario_id: uuid.UUID,
    solver_service: SolverService = Depends(get_solver_service),
    current_user: UserIncomingDto = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    try:
        return await solver_service.find_optimal_decision_pyagrum(session, scenario_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
