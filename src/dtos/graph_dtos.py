from pydantic import BaseModel
from typing import Optional
from src.models.edge import (
    Graph
)

class GraphDto(BaseModel):
    project_id: int
    name: str

class GraphIncomingDto(GraphDto):
    id: Optional[int]

class GraphOutgoingDto(GraphDto):
    id: int

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
    def to_outgoing_dtos(entities: list[Graph]) -> list[GraphOutgoingDto]:
        return [GraphMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[GraphIncomingDto], user_id: int) -> list[Graph]:
        return [GraphMapper.to_entity(dto, user_id) for dto in dtos]