from src.models import Edge
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy import select, and_, or_

class EdgeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Edge]) -> list[Edge]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, edges: list[Edge]) -> list[Edge]:
        """
        No idea if this actually works
        """
        conditions: list[ColumnElement[bool]] = [
            and_(Edge.lower_id == edge.lower_id, Edge.higher_id == edge.higher_id)
            for edge in edges
        ]
        
        query = select(Edge).where(or_(*conditions))
        result = await self.session.scalars(query)
        return list(result.all())
    
    async def get_all(self) -> list[Edge]:
        return list(
            (await self.session.scalars(select(Edge))).all()
        )
    
    async def delete(self, edges: list[Edge]) -> None:
        entities = await self.get(edges)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()

    async def update(self, edges: list[Edge]) -> list[Edge]:
        entities_to_update=await self.get(edges)
        for n, edge_to_update in enumerate(entities_to_update):
            edge=edges[n]
            edge_to_update.lower_id=edge.lower_id
            edge_to_update.higher_id=edge.higher_id
            edge_to_update.graph_id=edge.graph_id
        await self.session.flush()
        return entities_to_update