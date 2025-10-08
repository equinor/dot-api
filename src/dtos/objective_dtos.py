import uuid
from pydantic import BaseModel, Field
from typing import Annotated
from src.models.objective import Objective
from src.constants import (
    DatabaseConstants,
    ObjectiveTypes,
)


class ObjectiveDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)]
    description: Annotated[str, Field(max_length=DatabaseConstants.MAX_LONG_STRING_LENGTH.value)]

class ObjectiveViaScenarioDto(ObjectiveDto):
    """
    Class should only be a property of project when creating the project with objective(s)
    """
    type: ObjectiveTypes = ObjectiveTypes.FUNDAMENTAL


class ObjectiveIncomingDto(ObjectiveDto):
    scenario_id: uuid.UUID
    type: ObjectiveTypes = ObjectiveTypes.FUNDAMENTAL


class ObjectiveOutgoingDto(ObjectiveDto):
    scenario_id: uuid.UUID
    type: str


class ObjectiveMapper:
    @staticmethod
    def via_scenario_to_entity(
        dto: ObjectiveViaScenarioDto, user_id: int, senario_id: uuid.UUID
    ) -> Objective:
        return Objective(
            id=dto.id,
            scenario_id=senario_id,
            name=dto.name,
            type=dto.type,
            description=dto.description,
            user_id=user_id,
        )

    @staticmethod
    def to_outgoing_dto(entity: Objective) -> ObjectiveOutgoingDto:
        return ObjectiveOutgoingDto(
            id=entity.id,
            scenario_id=entity.scenario_id,
            name=entity.name,
            type=entity.type,
            description=entity.description,
        )

    @staticmethod
    def to_entity(dto: ObjectiveIncomingDto, user_id: int) -> Objective:
        return Objective(
            id=dto.id,
            scenario_id=dto.scenario_id,
            name=dto.name,
            type=dto.type,
            description=dto.description,
            user_id=user_id,
        )

    @staticmethod
    def via_scenario_to_entities(
        dtos: list[ObjectiveViaScenarioDto],
        user_id: int,
        scenario_id: uuid.UUID,
    ) -> list[Objective]:
        return [ObjectiveMapper.via_scenario_to_entity(dto, user_id, scenario_id) for dto in dtos]

    @staticmethod
    def to_outgoing_dtos(
        entities: list[Objective],
    ) -> list[ObjectiveOutgoingDto]:
        return [ObjectiveMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_entities(dtos: list[ObjectiveIncomingDto], user_id: int) -> list[Objective]:
        return [ObjectiveMapper.to_entity(dto, user_id) for dto in dtos]
