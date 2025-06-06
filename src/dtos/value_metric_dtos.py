from pydantic import BaseModel
from typing import Optional
from src.models.value_metric import (
    ValueMetric
)

class ValueMetricDto(BaseModel):
    name: str

class ValueMetricIncomingDto(ValueMetricDto):
    id: Optional[int]
    issue_id: Optional[int]

class ValueMetricOutgoingDto(ValueMetricDto):
    id: int
    issue_id: int

class ValueMetricMapper:
    @staticmethod
    def to_outgoing_dto(entity: ValueMetric) -> ValueMetricOutgoingDto:
        return ValueMetricOutgoingDto(
            id=entity.id,
            name=entity.name,
            issue_id=entity.issue_id
        )

    @staticmethod
    def to_entity(dto: ValueMetricIncomingDto) -> ValueMetric:
        return ValueMetric(
            id=dto.id,
            issue_id=dto.issue_id if dto.issue_id else None,
            name=dto.name,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[ValueMetric]) -> list[ValueMetricOutgoingDto]:
        return [ValueMetricMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[ValueMetricIncomingDto]) -> list[ValueMetric]:
        return [ValueMetricMapper.to_entity(dto) for dto in dtos]
    