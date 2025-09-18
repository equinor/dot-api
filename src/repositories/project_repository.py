import uuid
from src.models.project import Project
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository

class ProjectRepository(BaseRepository[Project, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Project, query_extension_method=QueryExtensions.load_project_with_relationships)

    async def update(self, entities: list[Project]) -> list[Project]:
        entities_to_update=await self.get([entity.id for entity in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.name=entity.name
            entity_to_update.project_role = [await self.session.merge(role) for role in entity.project_role]
            entity_to_update.description=entity.description
            
        await self.session.flush()
        return entities_to_update
