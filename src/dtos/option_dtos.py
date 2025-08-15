
import uuid
from pydantic import BaseModel, Field
from src.models.option import (
    Option
)

class OptionDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    decision_id: uuid.UUID
    utility: float
    

class OptionIncomingDto(OptionDto):
    pass

class OptionOutgoingDto(OptionDto):
    pass

class OptionMapper:
    @staticmethod
    def to_outgoing_dto(entity: Option) -> OptionOutgoingDto:
        return OptionOutgoingDto(
            id=entity.id,
            name=entity.name,
            decision_id=entity.decision_id,
            utility=entity.utility
        )

    @staticmethod
    def to_entity(dto: OptionIncomingDto) -> Option:
        return Option(
            id=dto.id,
            name=dto.name,
            decision_id=dto.decision_id,
            utility=dto.utility,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Option]) -> list[OptionOutgoingDto]:
        return [OptionMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OptionIncomingDto]) -> list[Option]:
        return [OptionMapper.to_entity(dto) for dto in dtos]