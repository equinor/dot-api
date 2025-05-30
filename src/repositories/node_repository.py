from src.models.node import Node
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class NodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Node]) -> list[Node]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Node]:
        query=select(Node).where(Node.id.in_(ids)).options(*QueryExtensions.load_node_with_relationships())
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def get_all(self) -> list[Node]:
        query=select(Node).options(*QueryExtensions.load_node_with_relationships())
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def update(self, entities: list[Node]) -> list[Node]:
        entities_to_update=await self.get([node.id for node in entities])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.scenario_id=entity.scenario_id
            if entity.issue_id:
                entity_to_update=entity.issue_id
            
        await self.session.flush()
        return entities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
