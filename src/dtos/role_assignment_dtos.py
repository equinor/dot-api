import uuid
from pydantic import BaseModel


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


