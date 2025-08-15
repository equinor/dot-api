

from src.models.project_owners import ProjectOwners
from src.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.query_extensions import QueryExtensions


class ProjectOwnersRepository(BaseRepository[ProjectOwners, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectOwners, query_extension_method=QueryExtensions.empty_load)

