import uuid
from pydantic import BaseModel
from src.constants import ProjectRoleType


class ProjectRoleDto(BaseModel):
    user_id: int
    project_id: uuid.UUID
    azure_id: uuid.UUID
    role: ProjectRoleType

class ProjectRoleIncomingDto(ProjectRoleDto):
  pass


