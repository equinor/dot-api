from src.models.edge import Edge
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class EdgeRepository(BaseRepository[Edge]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Edge, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[Edge]) -> list[Edge]:
        entities_to_update=await self.get([edge.id for edge in entities])
        for n, edge_to_update in enumerate(entities_to_update):
            edge=entities[n]
            edge_to_update.tail_id=edge.tail_id
            edge_to_update.head_id=edge.head_id
            edge_to_update.scenario_id=edge.scenario_id
        await self.session.flush()
        return entities_to_update