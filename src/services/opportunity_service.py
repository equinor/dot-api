from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.opportunity import Opportunity
from src.dtos.opportunity_dtos import (
    OpportunityIncomingDto, 
    OpportunityOutgoingDto, 
    OpportunityMapper
)
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.repositories.opportunity_repository import OpportunityRepository
from src.repositories.user_repository import UserRepository
from src.services.session_handler import session_handler

class OpportunityService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[OpportunityIncomingDto], user_dto: UserIncomingDto) -> list[OpportunityOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            entities: list[Opportunity] = await OpportunityRepository(session).create(OpportunityMapper.to_entities(dtos, user.id))
            # get the dtos while the entities are still connected to the session
            result: list[OpportunityOutgoingDto] = OpportunityMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[OpportunityIncomingDto], user_dto: UserIncomingDto) -> list[OpportunityOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            entities: list[Opportunity] = await OpportunityRepository(session).update(OpportunityMapper.to_entities(dtos, user.id))
            # get the dtos while the entities are still connected to the session
            result: list[OpportunityOutgoingDto] = OpportunityMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[int]):
        async with session_handler(self.engine) as session:
            await OpportunityRepository(session).delete(ids)
    
    async def get(self, ids: list[int]) -> list[OpportunityOutgoingDto]:
        async with session_handler(self.engine) as session:
            opportunities: list[Opportunity] = await OpportunityRepository(session).get(ids)
            result=OpportunityMapper.to_outgoing_dtos(opportunities)
        return result
    
    async def get_all(self) -> list[OpportunityOutgoingDto]:
        async with session_handler(self.engine) as session:
            opportunities: list[Opportunity] = await OpportunityRepository(session).get_all()
            result=OpportunityMapper.to_outgoing_dtos(opportunities)
        return result