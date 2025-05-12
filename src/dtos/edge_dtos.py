from pydantic import BaseModel
from src.models import (
    Edge
)

# Edge DTOs
class EdgeDto(BaseModel):
    lower_id: int
    higher_id: int
    graph_id: int

class EdgeMapper:
    @staticmethod
    def to_dto(entity: Edge) -> EdgeDto:
        return EdgeDto(
            lower_id=entity.lower_id,
            higher_id=entity.higher_id,
            graph_id=entity.graph_id
        )

    @staticmethod
    def to_entity(dto: EdgeDto) -> Edge:
        return Edge(
            lower_node_id=dto.lower_id,
            higher_node_id=dto.higher_id,
            graph_id=dto.graph_id
        )
    
    @staticmethod
    def to_dtos(entities: list[Edge]) -> list[EdgeDto]:
        return [EdgeMapper.to_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[EdgeDto]) -> list[Edge]:
        return [EdgeMapper.to_entity(dto) for dto in dtos]