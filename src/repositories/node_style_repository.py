import uuid
from src.models import NodeStyle
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions


class NodeStyleRepository(BaseRepository[NodeStyle, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session,
            NodeStyle,
            query_extension_method=QueryExtensions.empty_load,
        )

    async def update(self, entities: list[NodeStyle]) -> list[NodeStyle]:
        entities_to_update = await self.get([entity.id for entity in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.prepare_entities_for_update([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.x_position = entity.x_position
            entity_to_update.y_position = entity.y_position
            entity_to_update.width = entity.width
            entity_to_update.height = entity.height
            if entity.node_id:
                entity_to_update = entity.node_id

        await self.session.flush()
        return entities_to_update
