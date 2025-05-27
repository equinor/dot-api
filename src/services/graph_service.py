from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.graph import Graph
from src.dtos.graph_dtos import (
    GraphIncomingDto, 
    GraphOutgoingDto, 
    GraphMapper
)
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.repositories.graph_repository import GraphRepository
from src.repositories.user_repository import UserRepository

class GraphService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[GraphIncomingDto], user_dto: UserIncomingDto) -> list[GraphOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                entities: list[Graph] = await GraphRepository(session).create(GraphMapper.to_entities(dtos, user.id))
                # get the dtos while the entities are still connected to the session
                result: list[GraphOutgoingDto] = GraphMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def update(self, dtos: list[GraphIncomingDto], user_dto: UserIncomingDto) -> list[GraphOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                entities: list[Graph] = await GraphRepository(session).update(GraphMapper.to_entities(dtos, user.id))
                # get the dtos while the entities are still connected to the session
                result: list[GraphOutgoingDto] = GraphMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def delete(self, ids: list[int]):
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                await GraphRepository(session).delete(ids)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get(self, ids: list[int]) -> list[GraphOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            graphs: list[Graph] = await GraphRepository(session).get(ids)
            result=GraphMapper.to_outgoing_dtos(graphs)
        return result
    
    async def get_all(self) -> list[GraphOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            graphs: list[Graph] = await GraphRepository(session).get_all()
            result=GraphMapper.to_outgoing_dtos(graphs)
        return result
