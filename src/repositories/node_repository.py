from src.models.node import Node
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class NodeRepository(BaseRepository[Node]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Node, query_extension_method=QueryExtensions.load_node_with_relationships)

    async def update(self, entities: list[Node]) -> list[Node]:
        entities_to_update=await self.get([node.id for node in entities])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.scenario_id=entity.scenario_id
            if entity.issue_id:
                entity_to_update=entity.issue_id
            
        await self.session.flush()
        return entities_to_update
