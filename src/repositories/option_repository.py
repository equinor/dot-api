import uuid
from src.models.option import Option
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions


class OptionRepository(BaseRepository[Option, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Option, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[Option]) -> list[Option]:
        entities_to_update = await self.get([option.id for option in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.decision_id = entity.decision_id
            entity_to_update.name = entity.name
            entity_to_update.utility = entity.utility

        await self.session.flush()
        return entities_to_update
