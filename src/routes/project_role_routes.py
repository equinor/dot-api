import uuid
from fastapi import APIRouter, Depends, HTTPException
from src.services.user_service import get_current_user
from src.services.project_role_service import ProjectRoleService
from src.dependencies import  get_project_role_service
from src.dtos.user_dtos import UserIncomingDto

router = APIRouter(tags=["project-roles"])

@router.delete("/project-roles/{project_id}/{id}")
async def delete_opportunity(
    id: uuid.UUID,
    project_id: uuid.UUID,
    project_role_service: ProjectRoleService = Depends(get_project_role_service),
    current_user: UserIncomingDto = Depends(get_current_user)

):
    try:
        await project_role_service.delete(id, project_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))