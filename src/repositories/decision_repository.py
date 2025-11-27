import uuid
from src.models.decision import Decision
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions


class DecisionRepository(BaseRepository[Decision, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session,
            Decision,
            query_extension_method=QueryExtensions.load_decision_with_relationships,
        )

    async def update(self, entities: list[Decision]) -> list[Decision]:
        entities_to_update = await self.get([decision.id for decision in entities])
        # For update: sort and check that ids match between input and db entities
        self.prepare_entities_for_update([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update = await self._update_decision(entity, entity_to_update)
            
        await self.session.flush()
        return entities_to_update
