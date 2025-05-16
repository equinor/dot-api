from pydantic import BaseModel
from typing import Optional
from src.models import (
    Opportunity
)

class OpportunityDto(BaseModel):
    project_id: int
    name: str
    description: str

class OpportunityIncomingDto(OpportunityDto):
    id: Optional[int]

class OpportunityOutgoingDto(OpportunityDto):
    id: int

class OpportunityMapper:
    @staticmethod
    def to_outgoing_dto(entity: Opportunity) -> OpportunityOutgoingDto:
        return OpportunityOutgoingDto(
            id=entity.id,
            project_id=entity.project_id,
            name=entity.name,
            description=entity.description
        )

    @staticmethod
    def to_entity(dto: OpportunityIncomingDto, user_id: int) -> Opportunity:
        return Opportunity(
            id=dto.id,
            project_id=dto.project_id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Opportunity]) -> list[OpportunityOutgoingDto]:
        return [OpportunityMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OpportunityIncomingDto], user_id: int) -> list[Opportunity]:
        return [OpportunityMapper.to_entity(dto, user_id) for dto in dtos]