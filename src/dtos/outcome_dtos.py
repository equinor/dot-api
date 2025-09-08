
import uuid
from typing import Annotated, List
from pydantic import BaseModel, Field
from src.models.outcome import (
    Outcome
)
from src.constants import DatabaseConstants

from src.dtos.outcome_to_option_dtos import (
    OutcomeToOptionMapper,
    OutcomeToOptionIncomingDto,
)

from src.dtos.outcome_to_outcome_dtos import (
    OutcomeToOutcomeMapper,
    OutcomeToOutcomeIncomingDto,
)

class OutcomeDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)] = ""
    uncertainty_id: uuid.UUID
    probability: float = 0.
    utility: float = 0.
    

class OutcomeIncomingDto(OutcomeDto):
    parent_outcome_dto_ids: List[uuid.UUID]
    parent_option_dto_ids: List[uuid.UUID]

    @property
    def parent_outcome_dtos(self) -> List[OutcomeToOutcomeIncomingDto]:
        return [OutcomeToOutcomeIncomingDto(child_outcome_id=self.id, parent_outcome_id=x) for x in self.parent_outcome_dto_ids]        

    @property
    def parent_option_dtos(self) -> List[OutcomeToOptionIncomingDto]:
        return [OutcomeToOptionIncomingDto(child_outcome_id=self.id, parent_option_id=x) for x in self.parent_option_dto_ids]

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
            parent_options=OutcomeToOptionMapper.to_entities(dto.parent_option_dtos),
            parent_outcomes=OutcomeToOutcomeMapper.to_entities(dto.parent_outcome_dtos),
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Outcome]) -> list[OutcomeOutgoingDto]:
        return [OutcomeMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OutcomeIncomingDto]) -> list[Outcome]:
        return [OutcomeMapper.to_entity(dto) for dto in dtos]