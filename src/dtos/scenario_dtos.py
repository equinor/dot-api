from pydantic import BaseModel
from typing import Optional
from src.models.scenario import (
    Scenario
)
from src.dtos.opportunity_dtos import *
from src.dtos.objective_dtos import *

class ScenarioDto(BaseModel):
    name: str

class ScenarioCreateViaProjectDto(ScenarioDto):
    project_id: Optional[int]
    Objectives: list[ObjectiveViaScenarioDto]
    Opportunities: list[OpportunityViaProjectDto]

class ScenarioCreateDto(ScenarioDto):
    project_id: int
    Objectives: list[ObjectiveViaScenarioDto]
    Opportunities: list[OpportunityViaProjectDto]

class ScenarioIncomingDto(ScenarioDto):
    id: Optional[int]
    project_id: int
    Objectives: list[ObjectiveIncomingDto]
    Opportunities: list[OpportunityIncomingDto]

class ScenarioOutgoingDto(ScenarioDto):
    id: int
    project_id: int
    Objectives: list[ObjectiveOutgoingDto]
    Opportunities: list[OpportunityOutgoingDto]

class ScenarioMapper:
    @staticmethod
    def from_create_via_project_to_entity(dto: ScenarioCreateViaProjectDto, user_id: int, project_id: int) -> Scenario:
        return Scenario(
            id=None,
            name=dto.name,
            project_id=dto.project_id if dto.project_id is not None else project_id,
            user_id=user_id,
            opportunities=[], # must create the scenario first
            objectives=[], # must create the scenario first
        )
    
    @staticmethod
    def from_create_to_entity(dto: ScenarioCreateDto, user_id: int) -> Scenario:
        return Scenario(
            id=None,
            name=dto.name,
            project_id=dto.project_id,
            user_id=user_id,
            opportunities=[], # must create the scenario first
            objectives=[], # must create the scenario first
        )

    @staticmethod
    def to_outgoing_dto(entity: Scenario) -> ScenarioOutgoingDto:
        return ScenarioOutgoingDto(
            id=entity.id,
            project_id=entity.project_id,
            name=entity.name,
            Objectives=ObjectiveMapper.to_outgoing_dtos(entity.objectives),
            Opportunities=OpportunityMapper.to_outgoing_dtos(entity.opportunities),
        )

    @staticmethod
    def to_entity(dto: ScenarioIncomingDto, user_id: int) -> Scenario:
        return Scenario(
            id=dto.id,
            name=dto.name,
            project_id=dto.project_id,
            user_id=user_id,
            opportunities=OpportunityMapper.to_entities(dto.Opportunities, user_id),
            objectives=ObjectiveMapper.to_entities(dto.Objectives, user_id),
        )

    @staticmethod
    def from_create_via_project_to_entities(dtos: list[ScenarioCreateViaProjectDto], user_id: int, project_id: int) -> list[Scenario]:
        return [ScenarioMapper.from_create_via_project_to_entity(dto, user_id, project_id) for dto in dtos]
        
    @staticmethod
    def from_create_to_entities(dtos: list[ScenarioCreateDto], user_id: int) -> list[Scenario]:
        return [ScenarioMapper.from_create_to_entity(dto, user_id) for dto in dtos]
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Scenario]) -> list[ScenarioOutgoingDto]:
        return [ScenarioMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[ScenarioIncomingDto], user_id: int) -> list[Scenario]:
        return [ScenarioMapper.to_entity(dto, user_id) for dto in dtos]