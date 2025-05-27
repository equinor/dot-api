from pydantic import BaseModel
from src.models.edge import (
    Edge
)
from typing import Optional

# Edge DTOs
class EdgeDto(BaseModel):
    lower_id: int
    higher_id: int
    graph_id: int

class EdgeIncomingDto(EdgeDto):
    id: Optional[int]

class EdgeOutgoingDto(EdgeDto):
    id: int

class EdgeMapper:
    @staticmethod
    def to_outgoing_dto(entity: Edge) -> EdgeOutgoingDto:
        return EdgeOutgoingDto(
            id=entity.id,
            lower_id=entity.lower_id,
            higher_id=entity.higher_id,
            graph_id=entity.graph_id
        )

    @staticmethod
    def to_entity(dto: EdgeIncomingDto) -> Edge:
        return Edge(
            id=dto.id,
            lower_node_id=dto.lower_id,
            higher_node_id=dto.higher_id,
            graph_id=dto.graph_id
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Edge]) -> list[EdgeOutgoingDto]:
        return [EdgeMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[EdgeIncomingDto]) -> list[Edge]:
        return [EdgeMapper.to_entity(dto) for dto in dtos]