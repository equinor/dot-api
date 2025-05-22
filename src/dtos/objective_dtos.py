from pydantic import BaseModel
from typing import Optional
from src.models import (
    Objective
)

class ObjectiveDto(BaseModel):
    name: str
    description: str

class ObjectiveViaProjectDto(ObjectiveDto):
    """
    Class should only be a property of project when creating the project with objective(s)
    """
    pass

class ObjectiveIncomingDto(ObjectiveDto):
    id: Optional[int]
    project_id: int

class ObjectiveOutgoingDto(ObjectiveDto):
    id: int
    project_id: int

class ObjectiveMapper:
    @staticmethod
    def via_project_to_entity(dto: ObjectiveViaProjectDto, user_id: int, project_id: int) -> Objective:
        return Objective(
            id=None,
            project_id=project_id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
        )

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
    def via_project_to_entities(dtos: list[ObjectiveViaProjectDto], user_id: int, project_id: int) -> list[Objective]:
        return [ObjectiveMapper.via_project_to_entity(dto, user_id, project_id) for dto in dtos]
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Objective]) -> list[ObjectiveOutgoingDto]:
        return [ObjectiveMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[ObjectiveIncomingDto], user_id: int) -> list[Objective]:
        return [ObjectiveMapper.to_entity(dto, user_id) for dto in dtos]