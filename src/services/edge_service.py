import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine
from src.models import (
    Edge,
    Node,
)
from src.dtos.edge_dtos import (
    EdgeMapper,
    EdgeIncomingDto,
    EdgeOutgoingDto,
)
from src.repositories.edge_repository import EdgeRepository
from src.repositories.node_repository import NodeRepository
from src.services.session_handler import session_handler

class EdgeService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    @staticmethod
    def _connect_nodes_to_edge(edge: Edge, tail_node: Node, head_node: Node):
        edge.tail_node, edge.head_node = tail_node, head_node
        return edge

    async def create(self, dtos: list[EdgeIncomingDto]) -> list[EdgeOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Edge] = await EdgeRepository(session).create(EdgeMapper.to_entities(dtos))
            
            tail_nodes = await NodeRepository(session).get([x.tail_id for x in dtos])
            head_nodes = await NodeRepository(session).get([x.head_id for x in dtos])
            for edge, tail_node, head_node in zip(entities, tail_nodes, head_nodes):
                self._connect_nodes_to_edge(edge, tail_node, head_node)

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
    
    async def get_all(self, odata_query: Optional[str]=None) -> list[EdgeOutgoingDto]:
        async with session_handler(self.engine) as session:
            edges: list[Edge] = await EdgeRepository(session).get_all(odata_query=odata_query)
            result=EdgeMapper.to_outgoing_dtos(edges)
        return result
