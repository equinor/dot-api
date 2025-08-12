import uuid
from src.models.decision import Decision
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class DecisionRepository(BaseRepository[Decision, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Decision, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[Decision]) -> list[Decision]:
        entities_to_update=await self.get([decision.id for decision in entities])
        # sort the entity lists to share the same order according to the entity.id
        entities.sort(key=lambda entity: entity.id)
        entities_to_update.sort(key=lambda entity: entity.id)

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.alternatives=entity.alternatives
            if entity.issue_id:
                entity_to_update=entity.issue_id

        await self.session.flush()
        return entities_to_update
    