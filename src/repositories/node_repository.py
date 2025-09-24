import uuid
from src.models import Node
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository


class NodeRepository(BaseRepository[Node, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session, Node, query_extension_method=QueryExtensions.load_node_with_relationships,
        )

    async def update(self, entities: list[Node]) -> list[Node]:
        entities_to_update = await self.get([node.id for node in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.scenario_id = entity.scenario_id
            if entity.issue_id:
                entity_to_update.issue_id = entity.issue_id
            if entity.node_style:
                entity_to_update.node_style = await self.session.merge(entity.node_style)

        await self.session.flush()
        return entities_to_update
