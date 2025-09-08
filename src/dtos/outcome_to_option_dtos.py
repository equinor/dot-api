import uuid
from pydantic import BaseModel, Field
from src.models import (
    OutcomeToOption
)

class OutcomeToOptionDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    parent_option_id: uuid.UUID
    child_outcome_id: uuid.UUID

class OutcomeToOptionIncomingDto(OutcomeToOptionDto):
    pass

class OutcomeToOptionOutgoingDto(OutcomeToOptionDto):
    pass

class OutcomeToOptionMapper:
    @staticmethod
    def to_outgoing_dto(entity: OutcomeToOption) -> OutcomeToOptionOutgoingDto:
        return OutcomeToOptionOutgoingDto(
            id=entity.id,
            parent_option_id=entity.parent_option_id,
            child_outcome_id=entity.child_outcome_id,
        )

    @staticmethod
    def to_entity(dto: OutcomeToOptionIncomingDto) -> OutcomeToOption:
        return OutcomeToOption(
            id=dto.id,
            parent_option_id=dto.parent_option_id,
            child_outcome_id=dto.child_outcome_id,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[OutcomeToOption]) -> list[OutcomeToOptionOutgoingDto]:
        return [OutcomeToOptionMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OutcomeToOptionIncomingDto]) -> list[OutcomeToOption]:
        return [OutcomeToOptionMapper.to_entity(dto) for dto in dtos]