import uuid
from src.models.uncertainty import Uncertainty
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions


class UncertaintyRepository(BaseRepository[Uncertainty, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session,
            Uncertainty,
            query_extension_method=QueryExtensions.load_uncertainty_with_relationships,
        )

    async def update(self, entities: list[Uncertainty]) -> list[Uncertainty]:
        entities_to_update = await self.get([entity.id for entity in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.prepare_entities_for_update([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.outcomes = [
                await self.session.merge(outcome) for outcome in entity.outcomes
            ]
            entity_to_update.outcome_probabilities = [
                await self.session.merge(x) for x in entity.outcome_probabilities
            ]
            if entity.issue_id:
                entity_to_update.issue_id = entity.issue_id

        await self.session.flush()
        return entities_to_update
