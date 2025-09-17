from typing import Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from src.dtos.project_roles_dtos import   ProjectRoleIncomingDto, ProjectRoleOutgoingDto
from src.services.user_service import get_current_user
from src.services.project_role_service import ProjectRoleService
from src.dependencies import  get_project_role_service
from src.dtos.user_dtos import UserIncomingDto

router = APIRouter(tags=["project-roles"])
    
@router.get("/project-roles/")
async def get_all_project_roles(
    project_role_service: ProjectRoleService = Depends(get_project_role_service),
) -> list[ProjectRoleOutgoingDto]:
    try:
        project_roles: list[ProjectRoleOutgoingDto] = await project_role_service.get_all()
        return project_roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/project-roles/{id}")
async def get_project_role(
    id: uuid.UUID,
    project_role_service: ProjectRoleService = Depends(get_project_role_service),
) -> list[ProjectRoleOutgoingDto]:
    try:
        project_roles: list[ProjectRoleOutgoingDto] = await project_role_service.get([id])
        return project_roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/project-roles/{project_id}/{id}")
async def delete_project_role(
    id: uuid.UUID,
    project_id: uuid.UUID,
    project_role_service: ProjectRoleService = Depends(get_project_role_service),
    current_user: UserIncomingDto = Depends(get_current_user)

):
    try:
        await project_role_service.delete([id], project_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/project-roles/")
async def update_project_role(
    dto: list[ProjectRoleIncomingDto],
    project_role_service: ProjectRoleService = Depends(get_project_role_service),
    current_user: UserIncomingDto = Depends(get_current_user)
) -> Optional[list[ProjectRoleOutgoingDto]]:
    try:
        return await project_role_service.update( dto, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
