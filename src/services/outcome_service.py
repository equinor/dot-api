import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine
from src.models.outcome import Outcome
from src.dtos.outcome_dtos import (
    OutcomeIncomingDto, 
    OutcomeOutgoingDto, 
    OutcomeMapper
)
from src.repositories.outcome_repository import OutcomeRepository
from src.services.session_handler import session_handler

class OutcomeService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[OutcomeIncomingDto]) -> list[OutcomeOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Outcome] = await OutcomeRepository(session).create(OutcomeMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[OutcomeOutgoingDto] = OutcomeMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[OutcomeIncomingDto]) -> list[OutcomeOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Outcome] = await OutcomeRepository(session).update(OutcomeMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[OutcomeOutgoingDto] = OutcomeMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[uuid.UUID]):
        async with session_handler(self.engine) as session:
            await OutcomeRepository(session).delete(ids)
    
    async def get(self, ids: list[uuid.UUID]) -> list[OutcomeOutgoingDto]:
        async with session_handler(self.engine) as session:
            outcomes: list[Outcome] = await OutcomeRepository(session).get(ids)
            result=OutcomeMapper.to_outgoing_dtos(outcomes)
        return result
    
    async def get_all(self, odata_query: Optional[str]=None) -> list[OutcomeOutgoingDto]:
        async with session_handler(self.engine) as session:
            outcomes: list[Outcome] = await OutcomeRepository(session).get_all(odata_query=odata_query)
            result=OutcomeMapper.to_outgoing_dtos(outcomes)
        return result