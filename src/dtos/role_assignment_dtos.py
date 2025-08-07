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

class RoleAssignmentOutgoingDto():
    project_id: uuid.UUID
    project_name: str
    role:str


