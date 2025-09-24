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
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.options = [
                await self.session.merge(option) for option in entity.options
            ]
            if entity.issue_id:
                entity_to_update = entity.issue_id

        await self.session.flush()
        return entities_to_update
