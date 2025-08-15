import uuid
from pydantic import BaseModel, Field
from typing import List
from src.models.uncertainty import (
    Uncertainty
)

from src.dtos.outcome_dtos import (
    OutcomeIncomingDto,
    OutcomeOutgoingDto,
    OutcomeMapper,
)

class UncertaintyDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    issue_id: uuid.UUID

class UncertaintyIncomingDto(UncertaintyDto):
    outcomes: List[OutcomeIncomingDto]

class UncertaintyOutgoingDto(UncertaintyDto):
    outcomes: List[OutcomeOutgoingDto]

    
class UncertaintyMapper:
    @staticmethod
    def to_outgoing_dto(entity: Uncertainty) -> UncertaintyOutgoingDto:
        return UncertaintyOutgoingDto(
            id=entity.id,
            issue_id=entity.issue_id,
            outcomes=OutcomeMapper.to_outgoing_dtos(entity.outcomes),
        )

    @staticmethod
    def to_entity(dto: UncertaintyIncomingDto) -> Uncertainty:
        return Uncertainty(
            id=dto.id,
            issue_id=dto.issue_id,
            outcomes=OutcomeMapper.to_entities(dto.outcomes)
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Uncertainty]) -> list[UncertaintyOutgoingDto]:
        return [UncertaintyMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[UncertaintyIncomingDto]) -> list[Uncertainty]:
        return [UncertaintyMapper.to_entity(dto) for dto in dtos]