import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.node_style import NodeStyle
from src.dtos.node_style_dtos import (
    NodeStyleIncomingDto, 
    NodeStyleOutgoingDto, 
    NodeStyleMapper
)
from src.repositories.node_style_repository import NodeStyleRepository
from src.services.session_handler import session_handler

class NodeStyleService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[NodeStyleIncomingDto]) -> list[NodeStyleOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[NodeStyle] = await NodeStyleRepository(session).create(NodeStyleMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[NodeStyleOutgoingDto] = NodeStyleMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[NodeStyleIncomingDto]) -> list[NodeStyleOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[NodeStyle] = await NodeStyleRepository(session).update(NodeStyleMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[NodeStyleOutgoingDto] = NodeStyleMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[uuid.UUID]):
        async with session_handler(self.engine) as session:
            await NodeStyleRepository(session).delete(ids)
    
    async def get(self, ids: list[uuid.UUID]) -> list[NodeStyleOutgoingDto]:
        async with session_handler(self.engine) as session:
            node_styles: list[NodeStyle] = await NodeStyleRepository(session).get(ids)
            result=NodeStyleMapper.to_outgoing_dtos(node_styles)
        return result
    
    async def get_all(self, odata_query: Optional[str]=None) -> list[NodeStyleOutgoingDto]:
        async with session_handler(self.engine) as session:
            node_styles: list[NodeStyle] = await NodeStyleRepository(session).get_all(odata_query=odata_query)
            result=NodeStyleMapper.to_outgoing_dtos(node_styles)
        return result