

from src.models.project_role import ProjectRole
from src.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.query_extensions import QueryExtensions


class ProjectRoleRepository(BaseRepository[ProjectRole, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectRole, query_extension_method=QueryExtensions.empty_load)

