from pydantic import BaseModel
from typing import Optional
from src.models import (
    Graph
)
from src.dtos.node_dtos import *
from src.dtos.edge_dtos import *

class GraphDto(BaseModel):
    project_id: int
    name: str

class GraphIncomingDto(GraphDto):
    id: Optional[int]

class GraphOutgoingDto(GraphDto):
    id: int

class GraphModelDto(GraphDto):
    id: int
    nodes: list[NodeOutgoingDto]
    edges: list[EdgeOutgoingDto]


class GraphMapper:
    @staticmethod
    def to_outgoing_dto(entity: Graph) -> GraphOutgoingDto:
        return GraphOutgoingDto(
            id=entity.id,
            project_id=entity.project_id,
            name=entity.name
        )

    @staticmethod
    def to_entity(dto: GraphIncomingDto, user_id: int) -> Graph:
        return Graph(
            id=dto.id,
            name=dto.name,
            project_id=dto.project_id,
            user_id=user_id,
        )
    
    @staticmethod
    def to_dto_with_nodes(entity: Graph) -> GraphModelDto:
        return GraphModelDto(
            id=entity.id,
            project_id=entity.project_id,
            name=entity.name,
            nodes=NodeMapper.to_outgoing_dtos(entity.nodes),
            edges=EdgeMapper.to_outgoing_dtos(entity.edges),
        )

    @staticmethod
    def to_outgoing_dtos(entities: list[Graph]) -> list[GraphOutgoingDto]:
        return [GraphMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[GraphIncomingDto], user_id: int) -> list[Graph]:
        return [GraphMapper.to_entity(dto, user_id) for dto in dtos]
    
    @staticmethod
    def to_dtos_with_nodes(entities: list[Graph]) -> list[GraphModelDto]:
        return [GraphMapper.to_dto_with_nodes(entity) for entity in entities]