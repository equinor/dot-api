import uuid
from src.models.discrete_probability import DiscreteProbability
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions


class DiscreteProbabilityRepository(BaseRepository[DiscreteProbability, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session,
            DiscreteProbability,
            query_extension_method=QueryExtensions.load_discrete_probability_with_relationships,
        )

    async def update(self, entities: list[DiscreteProbability]) -> list[DiscreteProbability]:
        entities_to_update = await self.get([entity.id for entity in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.prepare_entities_for_update([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.probability = entity.probability
            entity_to_update.child_outcome_id = entity.child_outcome_id
            entity_to_update.uncertainty_id = entity.uncertainty_id
            
            # Update parent outcomes
            entity_to_update.parent_outcomes = [
                await self.session.merge(parent_outcome) for parent_outcome in entity.parent_outcomes
            ]
            
            # Update parent options
            entity_to_update.parent_options = [
                await self.session.merge(parent_option) for parent_option in entity.parent_options
            ]

        await self.session.flush()
        return entities_to_update
