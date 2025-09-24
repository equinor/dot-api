import uuid
from pydantic import BaseModel, Field
from typing import Annotated
from src.models.scenario import Scenario
from src.dtos.opportunity_dtos import (
    OpportunityMapper,
    OpportunityViaProjectDto,
    OpportunityIncomingDto,
    OpportunityOutgoingDto,
)
from src.dtos.objective_dtos import (
    ObjectiveMapper,
    ObjectiveViaScenarioDto,
    ObjectiveIncomingDto,
    ObjectiveOutgoingDto,
)
from src.dtos.issue_dtos import (
    IssueMapper,
    IssueOutgoingDto,
)
from src.dtos.edge_dtos import (
    EdgeMapper,
    EdgeOutgoingDto,
)
from src.constants import DatabaseConstants


class ScenarioDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: Annotated[
        str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)
    ] = ""
    is_default: bool = False


class ScenarioCreateViaProjectDto(ScenarioDto):
    objectives: list[ObjectiveViaScenarioDto]
    opportunities: list[OpportunityViaProjectDto]


class ScenarioCreateDto(ScenarioDto):
    project_id: uuid.UUID
    objectives: list[ObjectiveViaScenarioDto]
    opportunities: list[OpportunityViaProjectDto]


class ScenarioIncomingDto(ScenarioDto):
    project_id: uuid.UUID
    objectives: list[ObjectiveIncomingDto]
    opportunities: list[OpportunityIncomingDto]


class ScenarioOutgoingDto(ScenarioDto):
    project_id: uuid.UUID
    objectives: list[ObjectiveOutgoingDto]
    opportunities: list[OpportunityOutgoingDto]


class PopulatedScenarioDto(ScenarioOutgoingDto):
    project_id: uuid.UUID
    edges: list[EdgeOutgoingDto]
    issues: list[IssueOutgoingDto]


class ScenarioMapper:
    @staticmethod
    def from_create_via_project_to_entity(
        dto: ScenarioCreateViaProjectDto, user_id: int, project_id: uuid.UUID
    ) -> Scenario:
        return Scenario(
            id=dto.id,
            name=dto.name,
            is_default=dto.is_default,
            project_id=project_id,
            user_id=user_id,
            opportunities=[],  # must create the scenario first
            objectives=[],  # must create the scenario first
        )

    @staticmethod
    def from_create_to_entity(dto: ScenarioCreateDto, user_id: int) -> Scenario:
        return Scenario(
            id=dto.id,
            name=dto.name,
            is_default=dto.is_default,
            project_id=dto.project_id,
            user_id=user_id,
            opportunities=[],  # must create the scenario first
            objectives=[],  # must create the scenario first
        )

    @staticmethod
    def to_outgoing_dto(entity: Scenario) -> ScenarioOutgoingDto:
        return ScenarioOutgoingDto(
            id=entity.id,
            project_id=entity.project_id,
            name=entity.name,
            is_default=entity.is_default,
            objectives=ObjectiveMapper.to_outgoing_dtos(entity.objectives),
            opportunities=OpportunityMapper.to_outgoing_dtos(entity.opportunities),
        )

    @staticmethod
    def to_populated_dto(entity: Scenario) -> PopulatedScenarioDto:
        return PopulatedScenarioDto(
            id=entity.id,
            project_id=entity.project_id,
            name=entity.name,
            is_default=entity.is_default,
            objectives=ObjectiveMapper.to_outgoing_dtos(entity.objectives),
            opportunities=OpportunityMapper.to_outgoing_dtos(entity.opportunities),
            issues=IssueMapper.to_outgoing_dtos(entity.issues),
            edges=EdgeMapper.to_outgoing_dtos(entity.edges),
        )

    @staticmethod
    def to_entity(dto: ScenarioIncomingDto, user_id: int) -> Scenario:
        return Scenario(
            id=dto.id,
            name=dto.name,
            is_default=dto.is_default,
            project_id=dto.project_id,
            user_id=user_id,
            opportunities=OpportunityMapper.to_entities(dto.opportunities, user_id),
            objectives=ObjectiveMapper.to_entities(dto.objectives, user_id),
        )

    @staticmethod
    def from_create_via_project_to_entities(
        dtos: list[ScenarioCreateViaProjectDto], user_id: int, project_id: uuid.UUID
    ) -> list[Scenario]:
        return [
            ScenarioMapper.from_create_via_project_to_entity(dto, user_id, project_id)
            for dto in dtos
        ]

    @staticmethod
    def from_create_to_entities(
        dtos: list[ScenarioCreateDto], user_id: int
    ) -> list[Scenario]:
        return [ScenarioMapper.from_create_to_entity(dto, user_id) for dto in dtos]

    @staticmethod
    def to_outgoing_dtos(entities: list[Scenario]) -> list[ScenarioOutgoingDto]:
        return [ScenarioMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_populated_dtos(entities: list[Scenario]) -> list[PopulatedScenarioDto]:
        return [ScenarioMapper.to_populated_dto(entity) for entity in entities]

    @staticmethod
    def to_entities(dtos: list[ScenarioIncomingDto], user_id: int) -> list[Scenario]:
        return [ScenarioMapper.to_entity(dto, user_id) for dto in dtos]
