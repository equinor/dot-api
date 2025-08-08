import uuid
from pydantic import BaseModel
from src.dtos.project_dtos import ProjectDto
from src.models.project_contributors import (
    ProjectContributors
)

class RoleAssignmentDto(BaseModel):
        user_ids: list[int]
        project_id: uuid.UUID
        role: str

class RoleAssignmentIncomingDto(RoleAssignmentDto):
    pass

class RoleAssignmentOutgoingDto(BaseModel):
    project_id: uuid.UUID
    project_name: str
    role:str


# class RoleAssignmentMapper:
#     @staticmethod
#     def to_outgoing_dto(entity: RoleAssignment) -> RoleAssignmentOutgoingDto:
#         return RoleAssignmentOutgoingDto(
#             project_id=entity.project_id,
#             project_name=entity.project_name,
#             role=entity.role
#         )
