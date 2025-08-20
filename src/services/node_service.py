import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.node import Node
from src.dtos.node_dtos import (
    NodeIncomingDto, 
    NodeOutgoingDto, 
    NodeMapper
)
from src.repositories.node_repository import NodeRepository
from src.models.filters.node_filter import NodeFilter, node_conditions
from src.services.session_handler import session_handler

class NodeService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[NodeIncomingDto]) -> list[NodeOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Node] = await NodeRepository(session).create(NodeMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[NodeOutgoingDto] = NodeMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[NodeIncomingDto]) -> list[NodeOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Node] = await NodeRepository(session).update(NodeMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[NodeOutgoingDto] = NodeMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[uuid.UUID]):
        async with session_handler(self.engine) as session:
            await NodeRepository(session).delete(ids)
    
    async def get(self, ids: list[uuid.UUID]) -> list[NodeOutgoingDto]:
        async with session_handler(self.engine) as session:
            nodes: list[Node] = await NodeRepository(session).get(ids)
            result=NodeMapper.to_outgoing_dtos(nodes)
        return result
    
    async def get_all(self, filter: Optional[NodeFilter]=None, odata_query: Optional[str]=None) -> list[NodeOutgoingDto]:
        async with session_handler(self.engine) as session:
            model_filter = [NodeFilter.combine_conditions(node_conditions(filter))] if filter else []
            nodes: list[Node] = await NodeRepository(session).get_all(model_filter=model_filter, odata_query=odata_query)
            result=NodeMapper.to_outgoing_dtos(nodes)
        return result
    