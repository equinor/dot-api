from typing import List, Optional
from pydantic import BaseModel
from typing import List
from typing import Optional, List
from pydantic import BaseModel, Field
from src.dtos.issue_dtos import IssueOutgoingDto
import uuid

class EdgeUUIDDto(BaseModel):
    tail: uuid.UUID
    head: uuid.UUID | None

class EndPointNodeDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    scenario_id: uuid.UUID
    type: str = "EndPoint"

class DecisionTreeDTO(BaseModel):
    id: IssueOutgoingDto | EndPointNodeDto
    children: Optional[List["DecisionTreeDTO"]] = None
