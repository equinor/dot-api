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
            user_role = await ProjectRoleRepository(session).get_accessible_projects_by_user(azure_id=user_dto.azure_id)
            if not any(project_role.project_id == project_id and project_role.role == ProjectRoleType.OWNER for project_role in user_role):
                raise HTTPException(status_code=403, detail="Not authorized to delete this project role")
            await ProjectRoleRepository(session).delete(ids=[id])