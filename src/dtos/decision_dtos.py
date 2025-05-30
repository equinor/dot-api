from pydantic import BaseModel, Field
from typing import Optional, List
from src.models.decision import (
    Decision
)

class DecisionDto(BaseModel):
    options: List[str] = Field(default=[""])

class DecisionIncomingDto(DecisionDto):
    id: Optional[int] = Field(default=None, gt=0)
    issue_id: Optional[int]

class DecisionOutgoingDto(DecisionDto):
    id: int = Field(gt=0)
    issue_id: int


class DecisionMapper:
    @staticmethod
    def to_outgoing_dto(entity: Decision) -> DecisionOutgoingDto:
        return DecisionOutgoingDto(
            id=entity.id,
            issue_id=entity.issue_id,
            options=entity.options.split(",")
        )
    
    @staticmethod
    def to_entity(dto: DecisionIncomingDto) -> Decision:
        return Decision(
            id=dto.id,
            issue_id=dto.issue_id if dto.issue_id else None,
            options=",".join(dto.options)
        )

    @staticmethod
    def to_outgoing_dtos(entities: list[Decision]) -> list[DecisionOutgoingDto]:
        return [DecisionMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[DecisionIncomingDto]) -> list[Decision]:
        return [DecisionMapper.to_entity(dto) for dto in dtos]
