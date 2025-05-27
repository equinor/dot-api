from pydantic import BaseModel
from typing import Optional
from src.models.scenario import (
    Scenario
)

class ScenarioDto(BaseModel):
    project_id: int
    name: str

class ScenarioIncomingDto(ScenarioDto):
    id: Optional[int]

class ScenarioOutgoingDto(ScenarioDto):
    id: int

class ScenarioMapper:
    @staticmethod
    def to_outgoing_dto(entity: Scenario) -> ScenarioOutgoingDto:
        return ScenarioOutgoingDto(
            id=entity.id,
            project_id=entity.project_id,
            name=entity.name
        )

    @staticmethod
    def to_entity(dto: ScenarioIncomingDto, user_id: int) -> Scenario:
        return Scenario(
            id=dto.id,
            name=dto.name,
            project_id=dto.project_id,
            user_id=user_id,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Scenario]) -> list[ScenarioOutgoingDto]:
        return [ScenarioMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[ScenarioIncomingDto], user_id: int) -> list[Scenario]:
        return [ScenarioMapper.to_entity(dto, user_id) for dto in dtos]