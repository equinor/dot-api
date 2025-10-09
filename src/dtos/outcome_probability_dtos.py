import uuid
from typing import Annotated, List
from pydantic import BaseModel, Field
from src.models.outcome_probability import OutcomeProbability, OutcomeProbabilityParentOption, OutcomeProbabilityParentOutcome

class OutcomeProbabilityDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    uncertainty_id: uuid.UUID
    child_outcome_id: uuid.UUID
    probability: float = 0.0
    parent_outcome_ids: Annotated[List[uuid.UUID], Field(default_factory=list)] = []
    parent_option_ids: Annotated[List[uuid.UUID], Field(default_factory=list)] = []

class OutcomeProbabilityIncomingDto(OutcomeProbabilityDto):
    pass

class OutcomeProbabilityOutgoingDto(OutcomeProbabilityDto):
    pass

class OutcomeProbabilityMapper:
    @staticmethod
    def to_outgoing_dto(entity: OutcomeProbability) -> OutcomeProbabilityOutgoingDto:
        return OutcomeProbabilityOutgoingDto(
            id=entity.id,
            child_outcome_id=entity.child_outcome_id,
            uncertainty_id=entity.uncertainty_id,
            probability=entity.probability,
            parent_outcome_ids=[x.parent_outcome_id for x in entity.parent_outcomes] if entity.parent_outcomes else [],
            parent_option_ids=[x.parent_option_id for x in entity.parent_options] if entity.parent_options else [],
        )

    @staticmethod
    def to_entity(dto: OutcomeProbabilityIncomingDto) -> OutcomeProbability:
        return OutcomeProbability(
            id=dto.id,
            child_outcome_id=dto.child_outcome_id,
            uncertainty_id=dto.uncertainty_id,
            probability=dto.probability,
            parent_outcomes=[OutcomeProbabilityParentOutcome(outcome_probability_id=dto.child_outcome_id, parent_outcome_id=x) for x in dto.parent_outcome_ids],
            parent_options=[OutcomeProbabilityParentOption(outcome_probability_id=dto.child_outcome_id, parent_option_id=x) for x in dto.parent_option_ids]
        )

    @staticmethod
    def to_outgoing_dtos(entities: List[OutcomeProbability]) -> List[OutcomeProbabilityOutgoingDto]:
        return [OutcomeProbabilityMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_entities(dtos: List[OutcomeProbabilityIncomingDto]) -> List[OutcomeProbability]:
        return [OutcomeProbabilityMapper.to_entity(dto) for dto in dtos]