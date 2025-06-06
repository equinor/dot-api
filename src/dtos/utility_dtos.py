from pydantic import BaseModel
from typing import Optional, List
from src.models.utility import (
    Utility
)

class UtilityDto(BaseModel):
    values: List[float]

class UtilityIncomingDto(UtilityDto):
    id: Optional[int]
    issue_id: Optional[int]

class UtilityOutgoingDto(UtilityDto):
    id: int
    issue_id: int

class UtilityMapper:
    @staticmethod
    def to_outgoing_dto(entity: Utility) -> UtilityOutgoingDto:
        return UtilityOutgoingDto(
            id=entity.id,
            values=[float(p) for p in entity.values.split(",")],
            issue_id=entity.issue_id
        )

    @staticmethod
    def to_entity(dto: UtilityIncomingDto) -> Utility:
        return Utility(
            id=dto.id,
            issue_id=dto.issue_id if dto.issue_id else None,
            values=",".join(map(str, dto.values))
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Utility]) -> list[UtilityOutgoingDto]:
        return [UtilityMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[UtilityIncomingDto]) -> list[Utility]:
        return [UtilityMapper.to_entity(dto) for dto in dtos]