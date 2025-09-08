import uuid
from pydantic import BaseModel, Field
from src.models import (
    OptionToOption
)

class OptionToOptionDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    parent_option_id: uuid.UUID
    child_option_id: uuid.UUID
    edge_id: uuid.UUID

class OptionToOptionIncomingDto(OptionToOptionDto):
    pass

class OptionToOptionOutgoingDto(OptionToOptionDto):
    pass

class OptionToOptionMapper:
    @staticmethod
    def to_outgoing_dto(entity: OptionToOption) -> OptionToOptionOutgoingDto:
        return OptionToOptionOutgoingDto(
            id=entity.id,
            parent_option_id=entity.parent_option_id,
            child_option_id=entity.child_option_id,
            edge_id=entity.edge_id,
        )

    @staticmethod
    def to_entity(dto: OptionToOptionIncomingDto) -> OptionToOption:
        return OptionToOption(
            id=dto.id,
            parent_option_id=dto.parent_option_id,
            child_option_id=dto.child_option_id,
            edge_id=dto.edge_id,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[OptionToOption]) -> list[OptionToOptionOutgoingDto]:
        return [OptionToOptionMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OptionToOptionIncomingDto]) -> list[OptionToOption]:
        return [OptionToOptionMapper.to_entity(dto) for dto in dtos]