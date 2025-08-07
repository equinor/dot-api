
from http.client import HTTPException
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


class RoleAssignmentService:
    def __init__(self, async_engine: AsyncEngine):
        self.async_engine = async_engine

    async def assign_roles(self, dtos: RoleAssignmentDto, current_user: UserIncomingDto) -> RoleAssignmentOutgoingDto:
        if not dtos or not current_user:
            return None
        async with session_handler(self.async_engine) as session:
            accessible_project_ids = await UserRepository(session).get_accessible_projects_by_user(current_user.id)
            if not accessible_project_ids:
                return None
            if(dtos.project_id in accessible_project_ids.get("owner")):
               projects: list[Project] = await ProjectRepository(session).get([dtos.project_id])
               if(dtos.role == "contributor"):
                   await ProjectContributorsRepository(session).create(ProjectContributorMapper.from_role_to_entity(dtos))
                   return RoleAssignmentOutgoingDto(
                        project_id=dtos.project_id,
                        project_name=projects[0].name,
                        role=dtos.role
                    )
               elif(dtos.role == "owner"):
                   await ProjectOwnersRepository(session).create(ProjectOwnersMapper.from_role_to_entity(dtos))
                   return RoleAssignmentOutgoingDto(
                        project_id=dtos.project_id,
                        project_name=projects[0].name,
                        role=dtos.role
                    )
            else:
                raise HTTPException(status_code=403, detail="You do not have permission to assign roles for this project.")
        return None
