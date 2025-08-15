

from src.models.project_contributors import ProjectContributors
from src.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.query_extensions import QueryExtensions


class ProjectContributorsRepository(BaseRepository[ProjectContributors, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectContributors, query_extension_method=QueryExtensions.empty_load)

