from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
from src.models.decision import (
    Decision
)
from src.constants import DatabaseConstants

class DecisionDto(BaseModel):
    alternatives: List[Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)]] = [""]

class DecisionIncomingDto(DecisionDto):
    id: Optional[int] = Field(default=None, gt=0)
    issue_id: Optional[int]

class DecisionOutgoingDto(DecisionDto):
    id: int
    issue_id: int


class DecisionMapper:
    @staticmethod
    def to_outgoing_dto(entity: Decision) -> DecisionOutgoingDto:
        return DecisionOutgoingDto(
            id=entity.id,
            issue_id=entity.issue_id,
            alternatives=entity.alternatives.split(",")
        )
    
    @staticmethod
    def to_entity(dto: DecisionIncomingDto) -> Decision:
        return Decision(
            id=dto.id,
            issue_id=dto.issue_id if dto.issue_id else None,
            alternatives=",".join(dto.alternatives)
        )

    @staticmethod
    def to_outgoing_dtos(entities: list[Decision]) -> list[DecisionOutgoingDto]:
        return [DecisionMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[DecisionIncomingDto]) -> list[Decision]:
        return [DecisionMapper.to_entity(dto) for dto in dtos]
