import uuid
from src.models.uncertainty import Uncertainty
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class UncertaintyRepository(BaseRepository[Uncertainty, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Uncertainty, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[Uncertainty]) -> list[Uncertainty]:
        entities_to_update=await self.get([entity.id for entity in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.probabilities=entity.probabilities
            if entity.issue_id:
                entity_to_update=entity.issue_id
            
        await self.session.flush()
        return entities_to_update
    