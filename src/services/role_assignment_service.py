
from http.client import HTTPException
from typing import Optional

from sqlalchemy import Enum
from src.dtos.role_assignment_dtos import  RoleAssignmentDto, RoleAssignmentOutgoingDto
from src.dtos.project_contributors_dtos import  ProjectContributorMapper
from src.dtos.project_owners_dtos import  ProjectOwnersMapper
from src.dtos.user_dtos import UserIncomingDto
from sqlalchemy.ext.asyncio import  AsyncEngine
from src.models.project import Project
from src.repositories.project_owners_repository import ProjectOwnersRepository
from src.repositories.project_contributors_repository import ProjectContributorsRepository
from src.services.session_handler import session_handler
from src.repositories.project_repository import ProjectRepository
from src.repositories.user_repository import UserRepository

class ProjectRole(Enum):
    CONTRIBUTOR: str = "contributor"
    OWNER: str = "owner"
class RoleAssignmentService:
    def __init__(self, async_engine: AsyncEngine):
        self.async_engine = async_engine

    async def assign_roles(self, dtos: RoleAssignmentDto, current_user: UserIncomingDto) -> Optional[RoleAssignmentOutgoingDto]:
        if not dtos or not current_user:
            return None
        async with session_handler(self.async_engine) as session:
            accessible_project_ids = await UserRepository(session).get_accessible_projects_by_user(current_user.azure_id)
            if not accessible_project_ids:
                return None
            if dtos.project_id not in accessible_project_ids.owner_projects_ids:
                raise HTTPException(status_code=403, detail="You do not have permission to assign roles for this project.")
            projects: list[Project] = await ProjectRepository(session).get([dtos.project_id])
            if dtos.role == ProjectRole.CONTRIBUTOR:
                await ProjectContributorsRepository(session).create(ProjectContributorMapper.from_role_to_entity(dtos))
            elif dtos.role == ProjectRole.OWNER:
                await ProjectOwnersRepository(session).create(ProjectOwnersMapper.from_role_to_entity(dtos))
            else:
                return None
            return RoleAssignmentOutgoingDto(
                project_id=dtos.project_id,
                project_name=projects[0].name,
                role=dtos.role
            )
        return None
