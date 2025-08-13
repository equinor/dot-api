import uuid
from pydantic import BaseModel
from src.models.project_contributors import (
    ProjectContributors
)
from src.dtos.role_assignment_dtos import (
    RoleAssignmentIncomingDto,
)

class ProjectContributorDto(BaseModel):
        user_id: int
        project_id: list[uuid.UUID]


class ProjectContributorCreateDto(ProjectContributorDto):
    pass

class ProjectContributorOutgoingDto(ProjectContributorDto):
    pass

class ProjectContributorMapper:
    @staticmethod
    def from_role_to_entity(dto: RoleAssignmentIncomingDto) -> list[ProjectContributors]:
        project_contributors = [
            ProjectContributors(
                user_id=user_id,
                project_id=dto.project_id,
            )
            for user_id in dto.user_ids
        ]
        return project_contributors
      