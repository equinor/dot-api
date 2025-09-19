from typing import Optional
from src.repositories.user_repository import UserRepository
from src.models.project_role import ProjectRole
from src.dtos.project_roles_dtos import  ProjectRoleIncomingDto, ProjectRoleMapper, ProjectRoleOutgoingDto
from src.constants import ProjectRoleType
from src.dtos.user_dtos import UserIncomingDto
from src.repositories.project_role_repository import ProjectRoleRepository
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class ProjectRoleService:   
    async def delete(self, session: AsyncSession, role_ids: list[uuid.UUID], project_id: uuid.UUID, user_dto: UserIncomingDto) -> None:
        user = await UserRepository (session).get_by_azure_id(azure_id=user_dto.azure_id)
        if user is None or len(user.project_role) == 0:
                raise HTTPException(status_code=403, detail="User does not have any project roles")
        if not any(user_role_in_project.project_id == project_id for user_role_in_project in user.project_role):
            raise HTTPException(status_code=403, detail="Not authorized to delete this project role")

        await ProjectRoleRepository(session).delete(ids=role_ids)

    async def get(self, session: AsyncSession, project_role_ids: list[uuid.UUID]) -> list[ProjectRoleOutgoingDto]:
        project_roles = await ProjectRoleRepository(session).get(ids=project_role_ids)
        result: list[ProjectRoleOutgoingDto] = ProjectRoleMapper.to_outgoing_dtos(project_roles)
        return result  
         
    async def get_all(self, session: AsyncSession, ) -> list[ProjectRoleOutgoingDto]:
        project_roles = await ProjectRoleRepository(session).get_all()
        result: list[ProjectRoleOutgoingDto] = ProjectRoleMapper.to_outgoing_dtos(project_roles)
        return result   

    async def update(self, session: AsyncSession, dtos: list[ProjectRoleIncomingDto], current_user: UserIncomingDto) -> Optional[list[ProjectRoleOutgoingDto]]:
        user = await UserRepository(session).get_by_azure_id(azure_id=current_user.azure_id)
        for dto in dtos:
            if user is None or len(user.project_role) == 0:
                raise HTTPException(status_code=403, detail="User does not have any project roles")
            else:
                if not any(userRole.project_id == dto.project_id and userRole.role == ProjectRoleType.OWNER.value for userRole in user.project_role):
                    raise HTTPException(status_code=403, detail="Not authorized to update this project role")
        entities_project_role: list[ProjectRole] = await ProjectRoleRepository(session).update(ProjectRoleMapper.to_project_role_entities(dtos))
        result: list[ProjectRoleOutgoingDto] = ProjectRoleMapper.to_outgoing_dtos(entities_project_role)
        return result
