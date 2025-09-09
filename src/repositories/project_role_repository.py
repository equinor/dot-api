

from src.models.user import User
from src.models.project_role import ProjectRole
from src.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.repositories.query_extensions import QueryExtensions
import uuid


class ProjectRoleRepository(BaseRepository[ProjectRole, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectRole, query_extension_method=QueryExtensions.empty_load)

    async def get_accessible_projects_by_user(self, azure_id: str) -> list[ProjectRole] :
        self.query_extension_method = QueryExtensions.load_user_with_roles
        user_with_roles_stmt = select(User).where(User.azure_id == azure_id).options(
            *self.query_extension_method()
        )
        user_with_roles = (await self.session.scalars(user_with_roles_stmt)).first()
        project_roles: list[ProjectRole] = []
        if user_with_roles and hasattr(user_with_roles, "project_role"):
            project_roles.extend(user_with_roles.project_role)  

        return project_roles
