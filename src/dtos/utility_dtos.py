import uuid
from pydantic import BaseModel, Field
from typing import List
from src.models.utility import (
    Utility
)

class UtilityDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    issue_id: uuid.UUID
    values: List[float]

class UtilityIncomingDto(UtilityDto):
    pass

class UtilityOutgoingDto(UtilityDto):
    pass

class UtilityMapper:
    @staticmethod
    def to_outgoing_dto(entity: Utility) -> UtilityOutgoingDto:
        return UtilityOutgoingDto(
            id=entity.id,
            values = [float(p) for p in entity.values.split(",") if p.strip()] if entity.values else [],
            issue_id=entity.issue_id
        )

    @staticmethod
    def to_entity(dto: UtilityIncomingDto) -> Utility:
        return Utility(
            id=dto.id,
            issue_id=dto.issue_id,
            values=",".join(map(str, dto.values))
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Utility]) -> list[UtilityOutgoingDto]:
        return [UtilityMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[UtilityIncomingDto]) -> list[Utility]:
        return [UtilityMapper.to_entity(dto) for dto in dtos]