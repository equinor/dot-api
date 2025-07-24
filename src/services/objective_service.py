import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.objective import Objective
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
from src.services.session_handler import session_handler

class ObjectiveService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[ObjectiveIncomingDto], user_dto: UserIncomingDto) -> list[ObjectiveOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            entities: list[Objective] = await ObjectiveRepository(session).create(ObjectiveMapper.to_entities(dtos, user.id))
            # get the dtos while the entities are still connected to the session
            result: list[ObjectiveOutgoingDto] = ObjectiveMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[ObjectiveIncomingDto], user_dto: UserIncomingDto) -> list[ObjectiveOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            entities: list[Objective] = await ObjectiveRepository(session).update(ObjectiveMapper.to_entities(dtos, user.id))
            # get the dtos while the entities are still connected to the session
            result: list[ObjectiveOutgoingDto] = ObjectiveMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[uuid.UUID]):
        async with session_handler(self.engine) as session:
            await ObjectiveRepository(session).delete(ids)
    
    async def get(self, ids: list[uuid.UUID]) -> list[ObjectiveOutgoingDto]:
        async with session_handler(self.engine) as session:
            objectives: list[Objective] = await ObjectiveRepository(session).get(ids)
            result=ObjectiveMapper.to_outgoing_dtos(objectives)
        return result
    
    async def get_all(self, odata_query: Optional[str]=None) -> list[ObjectiveOutgoingDto]:
        async with session_handler(self.engine) as session:
            objectives: list[Objective] = await ObjectiveRepository(session).get_all(odata_query=odata_query)
            result=ObjectiveMapper.to_outgoing_dtos(objectives)
        return result