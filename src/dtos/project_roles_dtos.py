import uuid
from pydantic import BaseModel

from src.models.project_role import ProjectRole
from src.constants import ProjectRoleType


class ProjectRoleDto(BaseModel):
    user_name: str
    user_id: int
    project_id: uuid.UUID
    azure_id: uuid.UUID
    role: ProjectRoleType

class ProjectRoleIncomingDto(ProjectRoleDto):
  pass

class ProjectRoleOutgoingDto(BaseModel):
    user_name: str
    user_id: int
    project_id: uuid.UUID
    role: str



class ProjectRoleMapper:
    @staticmethod
    def from_create_to_entity(dto: ProjectRoleDto, user_id: int) -> ProjectRole:
        return ProjectRole(
            id=uuid.uuid4(),
            user_id=dto.user_id,
            project_id=dto.project_id,
            role=dto.role
        )
    @staticmethod
    def to_outgoing_dto(dto: ProjectRoleDto) -> ProjectRoleOutgoingDto:
        return ProjectRoleOutgoingDto(
            user_name=dto.user_name,
            user_id=dto.user_id,
            project_id=dto.project_id,
            role=dto.role
        )

    @staticmethod
    def from_create_via_project_to_entities(dtos: list[ProjectRoleDto], user_id: int, project_id: uuid.UUID) -> list[ProjectRole]:
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