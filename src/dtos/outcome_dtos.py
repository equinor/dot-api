import uuid
from typing import Annotated
from pydantic import BaseModel, Field
from src.models.outcome import Outcome
from src.constants import DatabaseConstants

class OutcomeDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)] = ""
    uncertainty_id: uuid.UUID
    utility: float = 0.0


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
            utility=entity.utility,
        )

    @staticmethod
    def to_entity(dto: OutcomeIncomingDto) -> Outcome:
        return Outcome(
            id=dto.id,
            name=dto.name,
            uncertainty_id=dto.uncertainty_id,
            utility=dto.utility,
        )

    @staticmethod
    def to_outgoing_dtos(entities: list[Outcome]) -> list[OutcomeOutgoingDto]:
        return [OutcomeMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_entities(dtos: list[OutcomeIncomingDto]) -> list[Outcome]:
        return [OutcomeMapper.to_entity(dto) for dto in dtos]
