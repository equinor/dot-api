import uuid
from pydantic import BaseModel, Field

from src.models.project_role import ProjectRole
from src.constants import ProjectRoleType

class UserInfoDto(BaseModel):
    user_name: str = Field(max_length=30)
    azure_id: str

class ProjectRoleDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: int
    project_id: uuid.UUID
    role: ProjectRoleType

class ProjectRoleIncomingDto(ProjectRoleDto, UserInfoDto):
    pass

class ProjectRoleCreateDto(ProjectRoleDto, UserInfoDto):
    pass

class ProjectRoleOutgoingDto(ProjectRoleDto, UserInfoDto):
    pass


class ProjectRoleMapper:
    @staticmethod
    def from_create_to_entity(dto: ProjectRoleCreateDto, user_id: int) -> ProjectRole:
        return ProjectRole(
            id=dto.id,
            user_id=dto.user_id,
            project_id=dto.project_id,
            role=dto.role
        )
    @staticmethod
    def to_project_role_entity(dto: ProjectRoleIncomingDto) -> ProjectRole:
        return ProjectRole(
            id=dto.id,
            user_id=dto.user_id,
            project_id=dto.project_id,
            role=dto.role
        )
    @staticmethod
    def to_outgoing_dto(dto: ProjectRoleOutgoingDto) -> ProjectRoleOutgoingDto:
        return ProjectRoleOutgoingDto(
            id=dto.id,
            user_name=dto.user_name,
            user_id=dto.user_id,
            project_id=dto.project_id,
            azure_id=dto.azure_id,
            role=dto.role
        )

    @staticmethod
    def from_create_via_project_to_entities(dtos: list[ProjectRoleCreateDto], user_id: int, project_id: uuid.UUID) -> list[ProjectRole]:
        if len(dtos) == 0:
            return [ProjectRole(
                id=uuid.uuid4(),
                user_id=user_id,
                project_id=project_id,
                role=ProjectRoleType.OWNER.value
            )]
        else:
            return [ProjectRoleMapper.from_create_to_entity(dto, user_id) for dto in dtos]
        
    @staticmethod
    def to_outgoing_dtos(entities: list[ProjectRole]) -> list[ProjectRoleOutgoingDto]:
        return [ProjectRoleMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_project_role_entities(entities: list[ProjectRoleIncomingDto]) -> list[ProjectRole]:
        return [ProjectRoleMapper.to_project_role_entity(entity) for entity in entities]