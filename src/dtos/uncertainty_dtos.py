import uuid
from pydantic import BaseModel, Field
from typing import List
from src.models.uncertainty import (
    Uncertainty
)

class UncertaintyDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    issue_id: uuid.UUID
    probabilities: List[float]

class UncertaintyIncomingDto(UncertaintyDto):
    pass

class UncertaintyOutgoingDto(UncertaintyDto):
    pass

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
            issue_id=dto.issue_id,
            probabilities=",".join(map(str, dto.probabilities))
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Uncertainty]) -> list[UncertaintyOutgoingDto]:
        return [UncertaintyMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[UncertaintyIncomingDto]) -> list[Uncertainty]:
        return [UncertaintyMapper.to_entity(dto) for dto in dtos]