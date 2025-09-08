import uuid
from pydantic import BaseModel, Field
from src.models import (
    OutcomeToOutcome
)

class OutcomeToOutcomeDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    parent_outcome_id: uuid.UUID
    child_outcome_id: uuid.UUID

class OutcomeToOutcomeIncomingDto(OutcomeToOutcomeDto):
    pass

class OutcomeToOutcomeOutgoingDto(OutcomeToOutcomeDto):
    pass

class OutcomeToOutcomeMapper:
    @staticmethod
    def to_outgoing_dto(entity: OutcomeToOutcome) -> OutcomeToOutcomeOutgoingDto:
        return OutcomeToOutcomeOutgoingDto(
            id=entity.id,
            parent_outcome_id=entity.parent_outcome_id,
            child_outcome_id=entity.child_outcome_id,
        )

    @staticmethod
    def to_entity(dto: OutcomeToOutcomeIncomingDto) -> OutcomeToOutcome:
        return OutcomeToOutcome(
            id=dto.id,
            parent_outcome_id=dto.parent_outcome_id,
            child_outcome_id=dto.child_outcome_id,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[OutcomeToOutcome]) -> list[OutcomeToOutcomeOutgoingDto]:
        return [OutcomeToOutcomeMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OutcomeToOutcomeIncomingDto]) -> list[OutcomeToOutcome]:
        return [OutcomeToOutcomeMapper.to_entity(dto) for dto in dtos]