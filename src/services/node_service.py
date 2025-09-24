import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.node import Node
from src.dtos.node_dtos import (
    NodeIncomingDto, 
    NodeOutgoingDto, 
    NodeMapper
)
from src.repositories.node_repository import NodeRepository
from src.models.filters.node_filter import NodeFilter

class NodeService:
    async def create(self, session: AsyncSession, dtos: list[NodeIncomingDto]) -> list[NodeOutgoingDto]:
        entities: list[Node] = await NodeRepository(session).create(NodeMapper.to_entities(dtos))
        # get the dtos while the entities are still connected to the session
        result: list[NodeOutgoingDto] = NodeMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, session: AsyncSession, dtos: list[NodeIncomingDto]) -> list[NodeOutgoingDto]:
        entities: list[Node] = await NodeRepository(session).update(NodeMapper.to_entities(dtos))
        # get the dtos while the entities are still connected to the session
        result: list[NodeOutgoingDto] = NodeMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, session: AsyncSession, ids: list[uuid.UUID]):
        await NodeRepository(session).delete(ids)
    
    async def get(self, session: AsyncSession, ids: list[uuid.UUID]) -> list[NodeOutgoingDto]:
        nodes: list[Node] = await NodeRepository(session).get(ids)
        result = NodeMapper.to_outgoing_dtos(nodes)
        return result
    
    async def get_all(self, session: AsyncSession, filter: Optional[NodeFilter] = None, odata_query: Optional[str] = None) -> list[NodeOutgoingDto]:
        model_filter = filter.construct_filters() if filter else []
        nodes: list[Node] = await NodeRepository(session).get_all(model_filter=model_filter, odata_query=odata_query)
        result = NodeMapper.to_outgoing_dtos(nodes)
        return result
