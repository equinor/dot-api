import uuid
from src.models.uncertainty import OutcomeProbability
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class OutcomeProbabilityRepository(BaseRepository[OutcomeProbability, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session,
            OutcomeProbability,
            query_extension_method=QueryExtensions.load_uncertainty_with_relationships,
        )

    async def update(self, entities: list[OutcomeProbability]) -> list[OutcomeProbability]:
        entities_to_update = await self.get([entity.id for entity in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.child_outcome_id = entity.child_outcome_id
            entity_to_update.uncertainty_id = entity.uncertainty_id
            entity_to_update.parent_outcomes = entity.parent_outcomes
            entity_to_update.parent_options = entity.parent_options

        await self.session.flush()
        return entities_to_update
