from src.models import Node
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
        return list(
            (await self.session.scalars(select(Node).where(Node.id.in_(ids)))).all()
        )
    
    async def get_all(self) -> list[Node]:
        return list(
            (await self.session.scalars(select(Node))).all()
        )
    
    async def update(self, entities: list[Node]) -> list[Node]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.graph_id=entity.graph_id
            enity_to_update.type=entity.type

            if (entity.decision is not None):
                enity_to_update.decision=entity.decision

            if (entity.probability is not None):
                enity_to_update.probability=entity.probability
            
        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
