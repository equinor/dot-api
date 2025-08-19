import uuid
from pydantic import BaseModel
from src.models.project_owners import (
    ProjectOwners
)

class ProjectOwnersDto(BaseModel):
        user_ids: list[int]
        project_id: uuid.UUID


class ProjectOwnersCreateDto(ProjectOwnersDto):
    pass

class ProjectsOwnerCreateDto(BaseModel):
    user_id: int
    project_ids: list[uuid.UUID]

class ProjectOwnersOutgoingDto(ProjectOwnersDto):
    pass

class ProjectOwnersMapper:
    @staticmethod
    def from_role_to_entity(dto: ProjectOwnersCreateDto) -> list[ProjectOwners]:
       project_owners = [
            ProjectOwners(
                user_id=user_id,
                project_id=dto.project_id,
            )
            for user_id in dto.user_ids
        ]
       return project_owners
    @staticmethod
    def from_role_to_entities(dto: ProjectsOwnerCreateDto) -> list[ProjectOwners]:
       project_owners = [
            ProjectOwners(
                user_id=dto.user_id,
                project_id=project_id,
            )
            for project_id in dto.project_ids
        ]
       return project_owners
