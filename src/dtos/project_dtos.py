import uuid
from pydantic import BaseModel, Field
from typing import Annotated
from src.dtos.project_roles_dtos import (
    ProjectRoleCreateDto,
    ProjectRoleIncomingDto,
    ProjectRoleMapper,
)
from src.models.project import Project
from src.dtos.scenario_dtos import (
    ScenarioMapper,
    ScenarioCreateViaProjectDto,
    ScenarioIncomingDto,
    ScenarioOutgoingDto,
    PopulatedScenarioDto,
)
from src.constants import DatabaseConstants

from src.dtos.project_roles_dtos import ProjectRoleOutgoingDto


class ProjectDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)] = ""
    description: Annotated[
        str, Field(max_length=DatabaseConstants.MAX_LONG_STRING_LENGTH.value)
    ] = ""


class ProjectCreateDto(ProjectDto):
    users: list[ProjectRoleCreateDto]
    scenarios: list[ScenarioCreateViaProjectDto]


class ProjectIncomingDto(ProjectDto):
    users: list[ProjectRoleIncomingDto]
    scenarios: list[ScenarioIncomingDto]


class ProjectOutgoingDto(ProjectDto):
    users: list[ProjectRoleOutgoingDto]
    scenarios: list[ScenarioOutgoingDto]


class PopulatedProjectDto(ProjectDto):
    users: list[ProjectRoleOutgoingDto]
    scenarios: list[PopulatedScenarioDto]


class ProjectMapper:
    @staticmethod
    def from_create_to_entity(dto: ProjectCreateDto, user_id: int) -> Project:
        return Project(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
            project_role=[],
            scenarios=[],  # must create the project first
        )

    @staticmethod
    def to_outgoing_dto(entity: Project) -> ProjectOutgoingDto:
        return ProjectOutgoingDto(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            users=ProjectRoleMapper.to_outgoing_dtos(entity.project_role),
            scenarios=ScenarioMapper.to_outgoing_dtos(entity.scenarios),
        )

    @staticmethod
    def to_populated_dto(entity: Project) -> PopulatedProjectDto:
        return PopulatedProjectDto(
            id=entity.id,
            name=entity.name,
            description=entity.name,
            users=ProjectRoleMapper.to_outgoing_dtos(entity.project_role),
            scenarios=ScenarioMapper.to_populated_dtos(entity.scenarios),
        )

    @staticmethod
    def to_project_entity(dto: ProjectIncomingDto, user_id: int) -> Project:
        return Project(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
            project_role=ProjectRoleMapper.to_project_role_entities(dto.users),
            scenarios=ScenarioMapper.to_entities(dto.scenarios, user_id),
        )

    @staticmethod
    def from_create_to_project_entities(
        dtos: list[ProjectCreateDto], user_id: int
    ) -> list[Project]:
        return [ProjectMapper.from_create_to_entity(dto, user_id) for dto in dtos]

    @staticmethod
    def to_outgoing_dtos(entities: list[Project]) -> list[ProjectOutgoingDto]:
        return [ProjectMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_populated_dtos(
        entities: list[Project],
    ) -> list[PopulatedProjectDto]:
        return [ProjectMapper.to_populated_dto(entity) for entity in entities]

    @staticmethod
    def to_project_entities(dtos: list[ProjectIncomingDto], user_id: int) -> list[Project]:
        return [ProjectMapper.to_project_entity(dto, user_id) for dto in dtos]
