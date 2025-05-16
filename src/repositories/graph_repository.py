from src.models import Graph
from src.models import Node
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class GraphRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Graph]) -> list[Graph]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Graph]:
        query=select(Graph).where(Graph.id.in_(ids)).options(
            selectinload(Graph.nodes).options(
                selectinload(Node.decision),
                selectinload(Node.probability),
            ),
            selectinload(Graph.edges),
        )
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def get_all(self) -> list[Graph]:
        return list(
            (await self.session.scalars(select(Graph))).all()
        )
    
    async def update(self, entities: list[Graph]) -> list[Graph]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.name=entity.name
            enity_to_update.project_id=entity.project_id
            
        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
