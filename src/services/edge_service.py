from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models import Edge
from src.dtos.edge_dtos import *
from src.repositories.edge_repository import EdgeRepository

class EdgeService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[EdgeIncomingDto]) -> list[EdgeOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                entities: list[Edge] = await EdgeRepository(session).create(EdgeMapper.to_entities(dtos))
                # get the dtos while the entities are still connected to the session
                result: list[EdgeOutgoingDto] = EdgeMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def update(self, dtos: list[EdgeIncomingDto]) -> list[EdgeOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                entities: list[Edge] = await EdgeRepository(session).update(EdgeMapper.to_entities(dtos))
                # get the dtos while the entities are still connected to the session
                result: list[EdgeOutgoingDto] = EdgeMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def delete(self, ids: list[int]):
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                await EdgeRepository(session).delete(ids)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get(self, ids: list[int]) -> list[EdgeOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            edges: list[Edge] = await EdgeRepository(session).get(ids)
            result=EdgeMapper.to_outgoing_dtos(edges)
        return result
    
    async def get_all(self) -> list[EdgeOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            edges: list[Edge] = await EdgeRepository(session).get_all()
            result=EdgeMapper.to_outgoing_dtos(edges)
        return result
