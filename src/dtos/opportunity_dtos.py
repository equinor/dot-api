from pydantic import BaseModel, Field
from typing import Optional, Annotated
from src.models.opportunity import (
    Opportunity
)
from src.constants import DatabaseConstants

class OpportunityDto(BaseModel):
    name: Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)] = ""
    description: Annotated[str, Field(max_length=DatabaseConstants.MAX_LONG_STRING_LENGTH.value)] = ""

class OpportunityViaProjectDto(OpportunityDto):
    """
    Class should only be a property of project when creating the project with opportunity(s)
    """
    pass


class OpportunityIncomingDto(OpportunityDto):
    id: Optional[int]
    scenario_id: int

class OpportunityOutgoingDto(OpportunityDto):
    id: int
    scenario_id: int

class OpportunityMapper:
    @staticmethod
    def via_project_to_entity(dto: OpportunityViaProjectDto, user_id: int, project_id: int) -> Opportunity:
        return Opportunity(
            id=None,
            scenario_id=project_id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
        )
    
    @staticmethod
    def to_outgoing_dto(entity: Opportunity) -> OpportunityOutgoingDto:
        return OpportunityOutgoingDto(
            id=entity.id,
            scenario_id=entity.scenario_id,
            name=entity.name,
            description=entity.description
        )

    @staticmethod
    def to_entity(dto: OpportunityIncomingDto, user_id: int) -> Opportunity:
        return Opportunity(
            id=dto.id,
            scenario_id=dto.scenario_id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
        )
    
    @staticmethod
    def via_project_to_entities(dtos: list[OpportunityViaProjectDto], user_id: int, project_id: int) -> list[Opportunity]:
        return [OpportunityMapper.via_project_to_entity(dto, user_id, project_id) for dto in dtos]
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Opportunity]) -> list[OpportunityOutgoingDto]:
        return [OpportunityMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OpportunityIncomingDto], user_id: int) -> list[Opportunity]:
        return [OpportunityMapper.to_entity(dto, user_id) for dto in dtos]