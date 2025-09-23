import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.node_style import NodeStyle
from src.dtos.node_style_dtos import (
    NodeStyleIncomingDto, 
    NodeStyleOutgoingDto, 
    NodeStyleMapper
)
from src.repositories.node_style_repository import NodeStyleRepository

class NodeStyleService:
    async def create(self, session: AsyncSession, dtos: list[NodeStyleIncomingDto]) -> list[NodeStyleOutgoingDto]:
        entities: list[NodeStyle] = await NodeStyleRepository(session).create(NodeStyleMapper.to_entities(dtos))
        # get the dtos while the entities are still connected to the session
        result: list[NodeStyleOutgoingDto] = NodeStyleMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, session: AsyncSession, dtos: list[NodeStyleIncomingDto]) -> list[NodeStyleOutgoingDto]:
        entities: list[NodeStyle] = await NodeStyleRepository(session).update(NodeStyleMapper.to_entities(dtos))
        # get the dtos while the entities are still connected to the session
        result: list[NodeStyleOutgoingDto] = NodeStyleMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, session: AsyncSession, ids: list[uuid.UUID]):
        await NodeStyleRepository(session).delete(ids)
    
    async def get(self, session: AsyncSession, ids: list[uuid.UUID]) -> list[NodeStyleOutgoingDto]:
        node_styles: list[NodeStyle] = await NodeStyleRepository(session).get(ids)
        result = NodeStyleMapper.to_outgoing_dtos(node_styles)
        return result
    
    async def get_all(self, session: AsyncSession, odata_query: Optional[str] = None) -> list[NodeStyleOutgoingDto]:
        node_styles: list[NodeStyle] = await NodeStyleRepository(session).get_all(odata_query=odata_query)
        result = NodeStyleMapper.to_outgoing_dtos(node_styles)
        return result
