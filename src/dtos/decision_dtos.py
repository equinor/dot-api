import uuid
from pydantic import BaseModel, Field
from typing import List
from src.models.decision import Decision
from src.dtos.option_dtos import (
    OptionIncomingDto,
    OptionOutgoingDto,
    OptionMapper,
)
from src.constants import DecisionHierarchy


class DecisionDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    issue_id: uuid.UUID


class DecisionIncomingDto(DecisionDto):
    options: List[OptionIncomingDto]
    type: DecisionHierarchy = DecisionHierarchy.FOCUS


class DecisionOutgoingDto(DecisionDto):
    options: List[OptionOutgoingDto]
    type: str


class DecisionMapper:
    @staticmethod
    def to_outgoing_dto(entity: Decision) -> DecisionOutgoingDto:
        return DecisionOutgoingDto(
            id=entity.id,
            issue_id=entity.issue_id,
            type=entity.type,
            options=OptionMapper.to_outgoing_dtos(entity.options),
        )

    @staticmethod
    def to_entity(dto: DecisionIncomingDto) -> Decision:
        return Decision(
            id=dto.id,
            issue_id=dto.issue_id,
            type=dto.type,
            options=OptionMapper.to_entities(dto.options),
        )

    @staticmethod
    def to_outgoing_dtos(
        entities: list[Decision],
    ) -> list[DecisionOutgoingDto]:
        return [DecisionMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_entities(dtos: list[DecisionIncomingDto]) -> list[Decision]:
        return [DecisionMapper.to_entity(dto) for dto in dtos]
