

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
            project_roles.extend(user_with_roles.project_role)  # Extend with user's project roles

        return project_roles

    async def get_or_create(self, entities: list[ProjectRole]) -> list[ProjectRole] | None:
        project_roles: list[ProjectRole] = []

        # Step 1: Fetch all existing ProjectRole instances
        scalar_result = await self.session.scalars(select(ProjectRole).where(ProjectRole.project_id == entities[0].project_id))
        all_roles = scalar_result.all()  # Get all ProjectRole instances
        existing_ids = {role.id for role in all_roles}  # Create a set of existing IDs

        # Step 2: Create a set of IDs from the input entities
        entity_ids = {entity.id for entity in entities}

        # Step 3: Delete roles that are not in the input entities
        ids_to_delete = existing_ids - entity_ids  # Find IDs to delete
        if len(ids_to_delete) > 0:
            await self.delete(list(ids_to_delete))

        # Step 4: Process the entities to get or create roles
        for entity in entities:
            scalar_result = await self.session.scalars(select(ProjectRole).where(ProjectRole.id == entity.id and ProjectRole.project_id == entity.project_id))
            project_role = scalar_result.first()
            if project_role is None:
                project_role = await self.create_single(entity)
                project_roles.append(project_role)
        if(len(entities) > 0):
            project_roles.extend(entities)
        return project_roles if len(project_roles) > 0 else None

    async def update(self, entities: list[ProjectRole]) -> list[ProjectRole]:
        entities_to_update=await self.get([entity.id for entity in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.user_id=entity.user_id
            entity_to_update.role=entity.role
            
        await self.session.flush()
        return entities_to_update
