import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine
from src.models.option import Option
from src.dtos.option_dtos import (
    OptionIncomingDto, 
    OptionOutgoingDto, 
    OptionMapper
)
from src.repositories.option_repository import OptionRepository
from src.services.session_handler import session_handler

class OptionService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[OptionIncomingDto]) -> list[OptionOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Option] = await OptionRepository(session).create(OptionMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[OptionOutgoingDto] = OptionMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[OptionIncomingDto]) -> list[OptionOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Option] = await OptionRepository(session).update(OptionMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[OptionOutgoingDto] = OptionMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[uuid.UUID]):
        async with session_handler(self.engine) as session:
            await OptionRepository(session).delete(ids)
    
    async def get(self, ids: list[uuid.UUID]) -> list[OptionOutgoingDto]:
        async with session_handler(self.engine) as session:
            options: list[Option] = await OptionRepository(session).get(ids)
            result=OptionMapper.to_outgoing_dtos(options)
        return result
    
    async def get_all(self, odata_query: Optional[str]=None) -> list[OptionOutgoingDto]:
        async with session_handler(self.engine) as session:
            options: list[Option] = await OptionRepository(session).get_all(odata_query=odata_query)
            result=OptionMapper.to_outgoing_dtos(options)
        return result