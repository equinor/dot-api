from pydantic import BaseModel
from typing import Optional
from src.models import (
    Objective
)

class ObjectiveDto(BaseModel):
    project_id: int
    name: str
    description: str

class ObjectiveIncomingDto(ObjectiveDto):
    id: Optional[int]

class ObjectiveOutgoingDto(ObjectiveDto):
    id: int

class ObjectiveMapper:
    @staticmethod
    def to_outgoing_dto(entity: Objective) -> ObjectiveOutgoingDto:
        return ObjectiveOutgoingDto(
            id=entity.id,
            project_id=entity.project_id,
            name=entity.name,
            description=entity.description
        )

    @staticmethod
    def to_entity(dto: ObjectiveIncomingDto, user_id: int) -> Objective:
        return Objective(
            id=dto.id,
            project_id=dto.project_id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Objective]) -> list[ObjectiveOutgoingDto]:
        return [ObjectiveMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[ObjectiveIncomingDto], user_id: int) -> list[Objective]:
        return [ObjectiveMapper.to_entity(dto, user_id) for dto in dtos]