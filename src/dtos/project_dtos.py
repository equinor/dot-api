from pydantic import BaseModel
from typing import Optional, List
from src.models.project import (
    Project
)
from src.dtos.objective_dtos import *
from src.dtos.opportunity_dtos import *

class ProjectDto(BaseModel):
    name: str
    description: str

class ProjectCreateDto(ProjectDto):
    Objectives: List[ObjectiveViaProjectDto]
    Opportunities: List[OpportunityViaProjectDto]

class ProjectIncomingDto(ProjectDto):
    id: Optional[int]
    Objectives: List[ObjectiveIncomingDto]
    Opportunities: List[OpportunityIncomingDto]

class ProjectOutgoingDto(ProjectDto):
    id: int
    Objectives: List[ObjectiveOutgoingDto]
    Opportunities: List[OpportunityOutgoingDto]

class ProjectMapper:
    @staticmethod
    def to_outgoing_dto(entity: Project) -> ProjectOutgoingDto:
        return ProjectOutgoingDto(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            Objectives=ObjectiveMapper.to_outgoing_dtos(entity.objectives),
            Opportunities=OpportunityMapper.to_outgoing_dtos(entity.opportunities)
        )

    @staticmethod
    def to_entity(dto: ProjectIncomingDto, user_id: int) -> Project:
        return Project(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
            opportunities=OpportunityMapper.to_entities(dto.Opportunities, user_id),
            objectives=ObjectiveMapper.to_entities(dto.Objectives, user_id)
        )
    
    @staticmethod
    def from_create_to_entity(dto: ProjectCreateDto, user_id: int) -> Project:
        return Project(
            id=None,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
            opportunities=[], # must create the project first
            objectives=[], # must create the project first
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Project]) -> list[ProjectOutgoingDto]:
        return [ProjectMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[ProjectIncomingDto], user_id: int) -> list[Project]:
        return [ProjectMapper.to_entity(dto, user_id) for dto in dtos]
    
    @staticmethod
    def from_create_to_entities(dtos: list[ProjectCreateDto], user_id: int) -> list[Project]:
        return [ProjectMapper.from_create_to_entity(dto, user_id) for dto in dtos]
