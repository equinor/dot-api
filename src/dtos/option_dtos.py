
import uuid
from typing import Annotated, List, Any
from pydantic import BaseModel, Field
from src.models import (
    Option,
    OptionToOption,
    OptionToOutcome
)
from src.dtos.option_to_option_dtos import (
    OptionToOptionMapper,
    OptionToOptionIncomingDto,
)
from src.dtos.option_to_outcome_dtos import (
    OptionToOutcomeIncomingDto,
    OptionToOutcomeMapper
)
from src.constants import DatabaseConstants

class OptionDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)] = ""
    decision_id: uuid.UUID
    utility: float = 0.
    

class OptionIncomingDto(OptionDto):
    parent_outcome_dto_ids: List[uuid.UUID]
    parent_option_dto_ids: List[uuid.UUID]

    @property
    def parent_outcome_dtos(self) -> List[OptionToOutcomeIncomingDto]:
        return [OptionToOutcomeIncomingDto(child_option_id=self.id, parent_outcome_id=x) for x in self.parent_outcome_dto_ids]        

    @property
    def parent_option_dtos(self) -> List[OptionToOptionIncomingDto]:
        return [OptionToOptionIncomingDto(child_option_id=self.id, parent_option_id=x) for x in self.parent_option_dto_ids]

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
            parent_options=OptionToOptionMapper.to_entities(dto.parent_option_dtos),
            parent_outcomes=OptionToOutcomeMapper.to_entities(dto.parent_outcome_dtos)
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Option]) -> list[OptionOutgoingDto]:
        return [OptionMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[OptionIncomingDto]) -> list[Option]:
        return [OptionMapper.to_entity(dto) for dto in dtos]