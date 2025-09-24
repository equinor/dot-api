import uuid
from pydantic import BaseModel, Field

from src.models.project_role import ProjectRole
from src.models.user import User
from src.constants import DatabaseConstants, ProjectRoleType


class UserInfoDto(BaseModel):
    user_name: str = Field(max_length=DatabaseConstants.MAX_LONG_STRING_LENGTH.value)
    azure_id: str


class ProjectRoleDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: int
    project_id: uuid.UUID


class ProjectRoleIncomingDto(ProjectRoleDto, UserInfoDto):
    role: ProjectRoleType


class ProjectRoleCreateDto(ProjectRoleDto, UserInfoDto):
    role: ProjectRoleType


class ProjectRoleOutgoingDto(ProjectRoleDto, UserInfoDto):
    role: str


class ProjectRoleMapper:
    @staticmethod
    def from_create_to_entity(dto: ProjectRoleCreateDto) -> ProjectRole:
        return ProjectRole(
            id=dto.id, user_id=dto.user_id, project_id=dto.project_id, role=dto.role,
        )

    @staticmethod
    def to_project_role_entity(dto: ProjectRoleIncomingDto) -> ProjectRole:
        return ProjectRole(
            id=dto.id,
            user_id=dto.user_id,
            project_id=dto.project_id,
            role=dto.role,
            user=User(id=dto.user_id, name=dto.user_name, azure_id=dto.azure_id),
        )

    @staticmethod
    def to_outgoing_dto(entity: ProjectRole) -> ProjectRoleOutgoingDto:
        return ProjectRoleOutgoingDto(
            id=entity.id,
            user_name=entity.user.name,
            user_id=entity.user_id,
            project_id=entity.project_id,
            azure_id=entity.user.azure_id,
            role=entity.role,
        )

    @staticmethod
    def from_create_via_project_to_entities(dtos: list[ProjectRoleCreateDto],) -> list[ProjectRole]:
        return [ProjectRoleMapper.from_create_to_entity(dto,) for dto in dtos]

    @staticmethod
    def to_outgoing_dtos(entities: list[ProjectRole],) -> list[ProjectRoleOutgoingDto]:
        return [ProjectRoleMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    def to_project_role_entities(entities: list[ProjectRoleIncomingDto],) -> list[ProjectRole]:
        return [ProjectRoleMapper.to_project_role_entity(entity) for entity in entities]
