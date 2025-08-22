import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine
from src.models.edge import Edge
from src.dtos.edge_dtos import (
    EdgeMapper,
    EdgeIncomingDto,
    EdgeOutgoingDto,
)
from src.models.filters.edge_filter import EdgeFilter
from src.repositories.edge_repository import EdgeRepository
from src.services.session_handler import session_handler

class EdgeService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[EdgeIncomingDto]) -> list[EdgeOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Edge] = await EdgeRepository(session).create(EdgeMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[EdgeOutgoingDto] = EdgeMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[EdgeIncomingDto]) -> list[EdgeOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Edge] = await EdgeRepository(session).update(EdgeMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[EdgeOutgoingDto] = EdgeMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[uuid.UUID]):
        async with session_handler(self.engine) as session:
            await EdgeRepository(session).delete(ids)
    
    async def get(self, ids: list[uuid.UUID]) -> list[EdgeOutgoingDto]:
        async with session_handler(self.engine) as session:
            edges: list[Edge] = await EdgeRepository(session).get(ids)
            result=EdgeMapper.to_outgoing_dtos(edges)
        return result
    
    async def get_all(self, odata_query: Optional[str]=None, filter: Optional[EdgeFilter]=None) -> list[EdgeOutgoingDto]:
        async with session_handler(self.engine) as session:
            model_filter = filter.construct_filters() if filter else []
            edges: list[Edge] = await EdgeRepository(session).get_all(odata_query=odata_query, model_filter=model_filter)
            result=EdgeMapper.to_outgoing_dtos(edges)
        return result
