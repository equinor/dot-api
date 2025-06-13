from pydantic import BaseModel
from typing import Optional

from src.models import NodeStyle

class NodeStyleDto(BaseModel):
    x_position: int = 0
    y_position: int = 0

class NodeStyleIncomingDto(NodeStyleDto):
    id: Optional[int] = None
    node_id: Optional[int] = None

class NodeStyleOutgoingDto(NodeStyleDto):
    id: int
    node_id: int

class NodeStyleMapper:
    @staticmethod
    def to_outgoing_dto(entity: NodeStyle) -> NodeStyleOutgoingDto:
        return NodeStyleOutgoingDto(
            id=entity.id,
            node_id=entity.node_id,
            x_position=entity.x_position,
            y_position=entity.y_position,
        )
    
    @staticmethod
    def to_entity(dto: NodeStyleIncomingDto) -> NodeStyle:
        return NodeStyle(
            id=dto.id,
            node_id=dto.node_id if dto.node_id else None,
            x_position=dto.x_position,
            y_position=dto.y_position,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[NodeStyle]) -> list[NodeStyleOutgoingDto]:
        return [NodeStyleMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[NodeStyleIncomingDto]) -> list[NodeStyle]:
        return [NodeStyleMapper.to_entity(dto) for dto in dtos]