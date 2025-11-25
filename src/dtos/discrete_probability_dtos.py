import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.discrete_probability import DiscreteProbability, DiscreteProbabilityParentOption, DiscreteProbabilityParentOutcome

class DiscreteProbabilityDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    uncertainty_id: uuid.UUID
    child_outcome_id: uuid.UUID
    probability: Optional[float] = None
    parent_outcome_ids: List[uuid.UUID] = []
    parent_option_ids: List[uuid.UUID] = []

class DiscreteProbabilityIncomingDto(DiscreteProbabilityDto):
    pass

class DiscreteProbabilityOutgoingDto(DiscreteProbabilityDto):
    pass

class DiscreteProbabilityMapper:
    @staticmethod
    def to_outgoing_dto(entity: DiscreteProbability) -> DiscreteProbabilityOutgoingDto:
        return DiscreteProbabilityOutgoingDto(
            id=entity.id,
            child_outcome_id=entity.child_outcome_id,
            uncertainty_id=entity.uncertainty_id,
            probability=entity.probability,
            parent_outcome_ids=[x.parent_outcome_id for x in entity.parent_outcomes] if entity.parent_outcomes else [],
            parent_option_ids=[x.parent_option_id for x in entity.parent_options] if entity.parent_options else [],
        )

    @staticmethod
    def to_entity(dto: DiscreteProbabilityIncomingDto) -> DiscreteProbability:
        return DiscreteProbability(
            id=dto.id,
            child_outcome_id=dto.child_outcome_id,
            uncertainty_id=dto.uncertainty_id,
            probability=dto.probability,
            parent_outcomes=[DiscreteProbabilityParentOutcome(discrete_probability_id=dto.id, parent_outcome_id=x) for x in dto.parent_outcome_ids],
            parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=dto.id, parent_option_id=x) for x in dto.parent_option_ids]
        )

    @staticmethod
    def to_outgoing_dtos(entities: List[DiscreteProbability]) -> List[DiscreteProbabilityOutgoingDto]:
        return [DiscreteProbabilityMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_entities(dtos: List[DiscreteProbabilityIncomingDto]) -> List[DiscreteProbability]:
        return [DiscreteProbabilityMapper.to_entity(dto) for dto in dtos]