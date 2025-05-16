from pydantic import BaseModel
from typing import Optional, List
from src.models import (
    Probability
)

class ProbabilityDto(BaseModel):
    probabilities: List[float]

class ProbabilityIncomingDto(ProbabilityDto):
    id: Optional[int]

class ProbabilityOutgoingDto(ProbabilityDto):
    id: int

class ProbabilityMapper:
    @staticmethod
    def to_outgoing_dto(entity: Probability) -> ProbabilityOutgoingDto:
        return ProbabilityOutgoingDto(
            id=entity.id,
            probabilities=[float(p) for p in entity.probabilities.split(",")]
        )

    @staticmethod
    def to_entity(dto: ProbabilityIncomingDto) -> Probability:
        return Probability(
            id=dto.id,
            probabilities=",".join(map(str, dto.probabilities))
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Probability]) -> list[ProbabilityOutgoingDto]:
        return [ProbabilityMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[ProbabilityIncomingDto]) -> list[Probability]:
        return [ProbabilityMapper.to_entity(dto) for dto in dtos]