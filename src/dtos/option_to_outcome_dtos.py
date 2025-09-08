import uuid
from pydantic import BaseModel, Field
from src.models import (
    OptionToOutcome
)

class OptionToOutcomeDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    parent_outcome_id: uuid.UUID
    child_option_id: uuid.UUID

class OptionToOutcomeIncomingDto(OptionToOutcomeDto):
    pass

class OptionToOutcomeOutgoingDto(OptionToOutcomeDto):
    pass

class OptionToOutcomeMapper:
    @staticmethod
    def to_outgoing_dto(entity: OptionToOutcome) -> OptionToOutcomeOutgoingDto:
        return OptionToOutcomeOutgoingDto(
            id=entity.id,
            parent_outcome_id=entity.parent_outcome_id,
            child_option_id=entity.child_option_id,
        )

    @staticmethod
    def to_entity(dto: OptionToOutcomeIncomingDto) -> OptionToOutcome:
        return OptionToOutcome(
            id=dto.id,
            parent_outcome_id=dto.parent_outcome_id,
            child_option_id=dto.child_option_id,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[OptionToOutcome]) -> list[OptionToOutcomeOutgoingDto]:
        return [OptionToOutcomeMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OptionToOutcomeIncomingDto]) -> list[OptionToOutcome]:
        return [OptionToOutcomeMapper.to_entity(dto) for dto in dtos]