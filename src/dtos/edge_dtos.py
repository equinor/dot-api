from pydantic import BaseModel
from src.models.edge import (
    Edge
)
from typing import Optional

# Edge DTOs
class EdgeDto(BaseModel):
    tail_id: int
    head_id: int
    scenario_id: int

class EdgeIncomingDto(EdgeDto):
    id: Optional[int]

class EdgeOutgoingDto(EdgeDto):
    id: int

class EdgeMapper:
    @staticmethod
    def to_outgoing_dto(entity: Edge) -> EdgeOutgoingDto:
        return EdgeOutgoingDto(
            id=entity.id,
            tail_id=entity.tail_id,
            head_id=entity.head_id,
            scenario_id=entity.scenario_id
        )

    @staticmethod
    def to_entity(dto: EdgeIncomingDto) -> Edge:
        return Edge(
            id=dto.id,
            tail_node_id=dto.tail_id,
            head_node_id=dto.head_id,
            scenario_id=dto.scenario_id
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Edge]) -> list[EdgeOutgoingDto]:
        return [EdgeMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[EdgeIncomingDto]) -> list[Edge]:
        return [EdgeMapper.to_entity(dto) for dto in dtos]