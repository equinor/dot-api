from pydantic import BaseModel
from typing import Optional
from src.models.project import (
    Project
)
from src.dtos.scenario_dtos import *

class ProjectDto(BaseModel):
    name: str
    description: str

class ProjectCreateDto(ProjectDto):
    scenarios: list[ScenarioCreateViaProjectDto]

class ProjectIncomingDto(ProjectDto):
    id: Optional[int]
    scenarios: list[ScenarioIncomingDto]

class ProjectOutgoingDto(ProjectDto):
    id: int
    scenarios: list[ScenarioOutgoingDto]

class ProjectMapper:
    @staticmethod
    def from_create_to_entity(dto: ProjectCreateDto, user_id: int) -> Project:
        return Project(
            id=None,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
            scenarios=[], # must create the project first
        )

    @staticmethod
    def to_outgoing_dto(entity: Project) -> ProjectOutgoingDto:
        return ProjectOutgoingDto(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            scenarios=ScenarioMapper.to_outgoing_dtos(entity.scenarios),
        )

    @staticmethod
    def to_entity(dto: ProjectIncomingDto, user_id: int) -> Project:
        return Project(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
            scenarios=ScenarioMapper.to_entities(dto.scenarios, user_id),
        )
    
    @staticmethod
    def from_create_to_entities(dtos: list[ProjectCreateDto], user_id: int) -> list[Project]:
        return [ProjectMapper.from_create_to_entity(dto, user_id) for dto in dtos]

    @staticmethod
    def to_outgoing_dtos(entities: list[Project]) -> list[ProjectOutgoingDto]:
        return [ProjectMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[ProjectIncomingDto], user_id: int) -> list[Project]:
        return [ProjectMapper.to_entity(dto, user_id) for dto in dtos]
    