from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.utility import Utility
from src.dtos.utility_dtos import (
    UtilityIncomingDto, 
    UtilityOutgoingDto, 
    UtilityMapper
)
from src.repositories.utility_repository import UtilityRepository
from src.services.session_handler import session_handler

class UtilityService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[UtilityIncomingDto]) -> list[UtilityOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Utility] = await UtilityRepository(session).create(UtilityMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[UtilityOutgoingDto] = UtilityMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[UtilityIncomingDto]) -> list[UtilityOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Utility] = await UtilityRepository(session).update(UtilityMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[UtilityOutgoingDto] = UtilityMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[int]):
        async with session_handler(self.engine) as session:
            await UtilityRepository(session).delete(ids)
    
    async def get(self, ids: list[int]) -> list[UtilityOutgoingDto]:
        async with session_handler(self.engine) as session:
            decisions: list[Utility] = await UtilityRepository(session).get(ids)
            result=UtilityMapper.to_outgoing_dtos(decisions)
        return result
    
    async def get_all(self) -> list[UtilityOutgoingDto]:
        async with session_handler(self.engine) as session:
            decisions: list[Utility] = await UtilityRepository(session).get_all()
            result=UtilityMapper.to_outgoing_dtos(decisions)
        return result