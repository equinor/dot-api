
import uuid
from pydantic import BaseModel, Field
from src.models.outcome import (
    Outcome
)

class OutcomeDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    uncertainty_id: uuid.UUID
    probability: float
    utility: float
    

class OutcomeIncomingDto(OutcomeDto):
    pass

class OutcomeOutgoingDto(OutcomeDto):
    pass

class OutcomeMapper:
    @staticmethod
    def to_outgoing_dto(entity: Outcome) -> OutcomeOutgoingDto:
        return OutcomeOutgoingDto(
            id=entity.id,
            name=entity.name,
            uncertainty_id=entity.uncertainty_id,
            probability=entity.probability,
            utility=entity.utility
        )

    @staticmethod
    def to_entity(dto: OutcomeIncomingDto) -> Outcome:
        return Outcome(
            id=dto.id,
            name=dto.name,
            uncertainty_id=dto.uncertainty_id,
            probability=dto.probability,
            utility=dto.utility,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Outcome]) -> list[OutcomeOutgoingDto]:
        return [OutcomeMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OutcomeIncomingDto]) -> list[Outcome]:
        return [OutcomeMapper.to_entity(dto) for dto in dtos]