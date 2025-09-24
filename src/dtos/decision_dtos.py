import uuid
from pydantic import BaseModel, Field
from typing import List
from src.models.decision import Decision
from src.dtos.option_dtos import OptionIncomingDto, OptionOutgoingDto, OptionMapper


class DecisionDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    issue_id: uuid.UUID


class DecisionIncomingDto(DecisionDto):
    options: List[OptionIncomingDto]


class DecisionOutgoingDto(DecisionDto):
    options: List[OptionOutgoingDto]


class DecisionMapper:
    @staticmethod
    def to_outgoing_dto(entity: Decision) -> DecisionOutgoingDto:
        return DecisionOutgoingDto(
            id=entity.id,
            issue_id=entity.issue_id,
            options=OptionMapper.to_outgoing_dtos(entity.options),
        )

    @staticmethod
    def to_entity(dto: DecisionIncomingDto) -> Decision:
        return Decision(
            id=dto.id,
            issue_id=dto.issue_id,
            options=OptionMapper.to_entities(dto.options),
        )

    @staticmethod
    def to_outgoing_dtos(entities: list[Decision]) -> list[DecisionOutgoingDto]:
        return [DecisionMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_entities(dtos: list[DecisionIncomingDto]) -> list[Decision]:
        return [DecisionMapper.to_entity(dto) for dto in dtos]
