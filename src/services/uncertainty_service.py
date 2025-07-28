import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.uncertainty import Uncertainty
from src.dtos.uncertainty_dtos import (
    UncertaintyIncomingDto, 
    UncertaintyOutgoingDto, 
    UncertaintyMapper
)
from src.repositories.uncertainty_repository import UncertaintyRepository
from src.services.session_handler import session_handler

class UncertaintyService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[UncertaintyIncomingDto]) -> list[UncertaintyOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Uncertainty] = await UncertaintyRepository(session).create(UncertaintyMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[UncertaintyOutgoingDto] = UncertaintyMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[UncertaintyIncomingDto]) -> list[UncertaintyOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Uncertainty] = await UncertaintyRepository(session).update(UncertaintyMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[UncertaintyOutgoingDto] = UncertaintyMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[uuid.UUID]):
        async with session_handler(self.engine) as session:
            await UncertaintyRepository(session).delete(ids)
    
    async def get(self, ids: list[uuid.UUID]) -> list[UncertaintyOutgoingDto]:
        async with session_handler(self.engine) as session:
            decisions: list[Uncertainty] = await UncertaintyRepository(session).get(ids)
            result=UncertaintyMapper.to_outgoing_dtos(decisions)
        return result
    
    async def get_all(self, odata_query: Optional[str]=None) -> list[UncertaintyOutgoingDto]:
        async with session_handler(self.engine) as session:
            decisions: list[Uncertainty] = await UncertaintyRepository(session).get_all(odata_query=odata_query)
            result=UncertaintyMapper.to_outgoing_dtos(decisions)
        return result