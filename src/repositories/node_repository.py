from src.models import Node
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class NodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Node]) -> list[Node]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Node]:
        query=select(Node).where(Node.id.in_(ids)).options(
            selectinload(Node.decision), 
            selectinload(Node.probability)
        )
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def get_all(self) -> list[Node]:
        query=select(Node).options(
            selectinload(Node.decision), 
            selectinload(Node.probability)
        )
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def update(self, entities: list[Node]) -> list[Node]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.graph_id=entity.graph_id
            enity_to_update.type=entity.type

            if (entity.decision is not None):
                enity_to_update.decision=await self.session.merge(entity.decision)

            if (entity.probability is not None):
                enity_to_update.probability=await self.session.merge(entity.probability)
            
        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
