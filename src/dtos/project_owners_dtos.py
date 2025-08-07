import uuid
from pydantic import BaseModel
from src.models.project_owners import (
    ProjectOwners
)

class ProjectOwnersDto(BaseModel):
        user_id: int
        project_id: list[uuid.UUID]


class ProjectOwnersCreateDto(ProjectOwnersDto):
    pass

class ProjectOwnersOutgoingDto(ProjectOwnersDto):
    pass

class ProjectOwnersMapper:
    @staticmethod
    def from_role_to_entity(dto: ProjectOwnersCreateDto) -> list[ProjectOwners]:
        owners = []
        for user_id in dto.user_ids:
            owners.append(ProjectOwners(
            user_id=user_id,
            project_id=dto.project_id,
            ))
        return owners