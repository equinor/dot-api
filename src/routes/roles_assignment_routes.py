
from fastapi import APIRouter, Depends, HTTPException

from src.dtos.project_dtos import ProjectOutgoingDto
from src.dtos.user_dtos import UserIncomingDto
from services.role_assignment_service import RoleAssignmentService
from src.services.user_service import get_current_user
from src.dependencies import get_role_service
from src.dtos.role_assignment_dtos import RoleAssignmentIncomingDto


router = APIRouter(tags=["rolesassignment"])

@router.post("/assign-roles")
async def assign_roles(
    dtos: RoleAssignmentIncomingDto,
    role_service: RoleAssignmentService = Depends(get_role_service),
    current_user: UserIncomingDto = Depends(get_current_user)
)-> list[ProjectOutgoingDto]:
    try:
        return list(await role_service.assign_roles(dtos, current_user))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
