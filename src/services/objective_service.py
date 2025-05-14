from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models import Objective
from src.dtos.objective_dtos import (
    ObjectiveIncomingDto, 
    ObjectiveOutgoingDto, 
    ObjectiveMapper
)
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.repositories.objective_repository import ObjectiveRepository
from src.repositories.user_repository import UserRepository

class ObjectiveService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[ObjectiveIncomingDto], user_dto: UserIncomingDto) -> list[ObjectiveOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                entities: list[Objective] = await ObjectiveRepository(session).create(ObjectiveMapper.to_entities(dtos, user.id))
                # get the dtos while the entities are still connected to the session
                result: list[ObjectiveOutgoingDto] = ObjectiveMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def update(self, dtos: list[ObjectiveIncomingDto], user_dto: UserIncomingDto) -> list[ObjectiveOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                entities: list[Objective] = await ObjectiveRepository(session).update(ObjectiveMapper.to_entities(dtos, user.id))
                # get the dtos while the entities are still connected to the session
                result: list[ObjectiveOutgoingDto] = ObjectiveMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def delete(self, ids: list[int]):
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                await ObjectiveRepository(session).delete(ids)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get(self, ids: list[int]) -> list[ObjectiveOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            objectives: list[Objective] = await ObjectiveRepository(session).get(ids)
            result=ObjectiveMapper.to_outgoing_dtos(objectives)
        return result
    
    async def get_all(self) -> list[ObjectiveOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            objectives: list[Objective] = await ObjectiveRepository(session).get_all()
            result=ObjectiveMapper.to_outgoing_dtos(objectives)
        return result