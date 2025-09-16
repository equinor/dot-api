

from src.models.user import User
from src.models.project_role import ProjectRole
from src.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.repositories.query_extensions import QueryExtensions
import uuid


class ProjectRoleRepository(BaseRepository[ProjectRole, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectRole, query_extension_method=QueryExtensions.load_role_with_user)

    async def get_accessible_projects_by_user(self, azure_id: str) -> list[ProjectRole] :
        self.query_extension_method = QueryExtensions.load_user_with_roles
        user_with_roles_stmt = select(User).where(User.azure_id == azure_id).options(
           *self.query_extension_method()
        )
        user_with_roles = (await self.session.scalars(user_with_roles_stmt)).all()
        project_roles: list[ProjectRole] = []
        for user in user_with_roles:
            if hasattr(user, "project_role"):
                project_roles.extend(user.project_role)

        return project_roles
    
    async def update(self, entities: list[ProjectRole]) -> list[ProjectRole]:
        entities_to_update=await self.get([entity.id for entity in entities])
        self.sort_entity_collections_by_id([entities, entities_to_update])
        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.user=entity.user
            entity_to_update.role = entity.role
            entity_to_update.project_id=entity.project_id
        await self.session.flush()
        return entities_to_update

