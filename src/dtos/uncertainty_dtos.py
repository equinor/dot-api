from pydantic import BaseModel
from typing import Optional, List
from src.models.uncertainty import (
    Uncertainty
)

class UncertaintyDto(BaseModel):
    probabilities: List[float]

class UncertaintyIncomingDto(UncertaintyDto):
    id: Optional[int]
    issue_id: Optional[int]

class UncertaintyOutgoingDto(UncertaintyDto):
    id: int
    issue_id: int

class UncertaintyMapper:
    @staticmethod
    def to_outgoing_dto(entity: Uncertainty) -> UncertaintyOutgoingDto:
        return UncertaintyOutgoingDto(
            id=entity.id,
            probabilities=[float(p) for p in entity.probabilities.split(",")],
            issue_id=entity.issue_id,
        )

    @staticmethod
    def to_entity(dto: UncertaintyIncomingDto) -> Uncertainty:
        return Uncertainty(
            id=dto.id,
            issue_id=dto.issue_id if dto.issue_id else None,
            probabilities=",".join(map(str, dto.probabilities))
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Uncertainty]) -> list[UncertaintyOutgoingDto]:
        return [UncertaintyMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[UncertaintyIncomingDto]) -> list[Uncertainty]:
        return [UncertaintyMapper.to_entity(dto) for dto in dtos]