import uuid
from pydantic import BaseModel, Field
from typing import List
from src.models.uncertainty import Uncertainty

from src.dtos.outcome_dtos import (
    OutcomeIncomingDto,
    OutcomeOutgoingDto,
    OutcomeMapper,
)

from src.dtos.discrete_probability_dtos import (
    DiscreteProbabilityIncomingDto,
    DiscreteProbabilityOutgoingDto,
    DiscreteProbabilityMapper,
)


class UncertaintyDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    issue_id: uuid.UUID
    is_key: bool = True


class UncertaintyIncomingDto(UncertaintyDto):
    discrete_probabilities: list[DiscreteProbabilityIncomingDto] = []
    outcomes: List[OutcomeIncomingDto] = []


class UncertaintyOutgoingDto(UncertaintyDto):
    discrete_probabilities: list[DiscreteProbabilityOutgoingDto] = []
    outcomes: List[OutcomeOutgoingDto] = []


class UncertaintyMapper:
    @staticmethod
    def to_outgoing_dto(entity: Uncertainty) -> UncertaintyOutgoingDto:
        return UncertaintyOutgoingDto(
            id=entity.id,
            issue_id=entity.issue_id,
            is_key=entity.is_key,
            outcomes=OutcomeMapper.to_outgoing_dtos(entity.outcomes),
            discrete_probabilities=DiscreteProbabilityMapper.to_outgoing_dtos(entity.discrete_probabilities),
        )

    @staticmethod
    def to_entity(dto: UncertaintyIncomingDto) -> Uncertainty:
        return Uncertainty(
            id=dto.id,
            issue_id=dto.issue_id,
            is_key=dto.is_key,
            outcomes=OutcomeMapper.to_entities(dto.outcomes),
            discrete_probabilities=DiscreteProbabilityMapper.to_entities(dto.discrete_probabilities),
        )

    @staticmethod
    def to_outgoing_dtos(
        entities: list[Uncertainty],
    ) -> list[UncertaintyOutgoingDto]:
        return [UncertaintyMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_entities(dtos: list[UncertaintyIncomingDto]) -> list[Uncertainty]:
        return [UncertaintyMapper.to_entity(dto) for dto in dtos]
