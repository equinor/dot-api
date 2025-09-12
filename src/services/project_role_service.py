from models.project_role import ProjectRole
from src.dtos.project_roles_dtos import ProjectRoleIncomingDto, ProjectRoleMapper, ProjectRoleOutgoingDto
from src.constants import ProjectRoleType
from src.dtos.user_dtos import UserIncomingDto
from src.repositories.project_role_repository import ProjectRoleRepository
from src.services.session_handler import session_handler
import uuid
from sqlalchemy.ext.asyncio import  AsyncEngine
from fastapi import HTTPException


class ProjectRoleService:   
    def __init__(self, engine: AsyncEngine):
        self.engine: AsyncEngine = engine

    async def delete(self, id: uuid.UUID, project_id: uuid.UUID, user_dto: UserIncomingDto) -> None:
        async with session_handler(self.engine) as session:
            user_role_in_projects = await ProjectRoleRepository(session).get_accessible_projects_by_user(azure_id=user_dto.azure_id)
            if not any(project_role.project_id == project_id and project_role.role == ProjectRoleType.OWNER for project_role in user_role_in_projects):
                raise HTTPException(status_code=403, detail="Not authorized to delete this project role")
            await ProjectRoleRepository(session).delete(ids=[id])

    async def update(self, dtos: list[ProjectRoleIncomingDto], current_user: UserIncomingDto) -> list[ProjectRoleOutgoingDto]:
        async with session_handler(self.engine) as session:
            user_role_in_projects = await ProjectRoleRepository(session).get_accessible_projects_by_user(azure_id=current_user.azure_id)
            for dto in dtos:
                if not any(project_role.project_id == dto.project_id and project_role.role == ProjectRoleType.OWNER for project_role in user_role_in_projects):
                    raise HTTPException(status_code=403, detail="Not authorized to update this project role")
            entities_project: list[ProjectRole] = await ProjectRoleRepository(session).update(ProjectRoleMapper.to_project_role_entities(dtos))
            result: list[ProjectRoleOutgoingDto] = ProjectRoleMapper.to_outgoing_dtos(entities_project)
            return result
