from pydantic import BaseModel, Field
from typing import Optional, List
from src.models import (
    Decision
)

class DecisionDto(BaseModel):
    options: List[str] = Field(default=[""])

class DecisionIncomingDto(DecisionDto):
    id: Optional[int] = Field(default=None, gt=0)

class DecisionOutgoingDto(DecisionDto):
    id: int = Field(gt=0)


class DecisionMapper:
    @staticmethod
    def to_outgoing_dto(entity: Decision) -> DecisionOutgoingDto:
        return DecisionOutgoingDto(
            id=entity.id,
            options=entity.options.split(",")
        )
    
    @staticmethod
    def to_entity(dto: DecisionIncomingDto) -> Decision:
        return Decision(
            id=dto.id,
            options=",".join(dto.options)
        )

    @staticmethod
    def to_outgoing_dtos(entities: list[Decision]) -> list[DecisionOutgoingDto]:
        return [DecisionMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[DecisionIncomingDto]) -> list[Decision]:
        return [DecisionMapper.to_entity(dto) for dto in dtos]
