from pydantic import BaseModel
from typing import Optional, List
from src.models import (
    Project
)
from src.dtos.objective_dtos import *
from src.dtos.opportunity_dtos import *

class ProjectDto(BaseModel):
    name: str
    description: str
    Objectives: List[ObjectiveDto]
    Opportunities: List[OpportunityDto]

class ProjectIncomingDto(ProjectDto):
    id: Optional[int]

class ProjectOutgoingDto(ProjectDto):
    id: int

class ProjectMapper:
    @staticmethod
    def to_outgoing_dto(entity: Project) -> ProjectOutgoingDto:
        return ProjectOutgoingDto(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            Objectives=[ObjectiveMapper.to_outgoing_dto(obj) for obj in entity.get_objectives()],
            Opportunities=[OpportunityMapper.to_outgoing_dto(opp) for opp in entity.get_oppertunities()]
        )

    @staticmethod
    def to_entity(dto: ProjectIncomingDto, user_id: int) -> Project:
        return Project(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Project]) -> list[ProjectOutgoingDto]:
        return [ProjectMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[ProjectIncomingDto], user_id: int) -> list[Project]:
        return [ProjectMapper.to_entity(dto, user_id) for dto in dtos]