import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from src.dtos.issue_dtos import IssueOutgoingDto
#from src.services.decision_tree.decision_tree_creator2 import NodeProtocol


class EdgeUUIDDto(BaseModel):
    tail: uuid.UUID
    head: uuid.UUID | None


class EndPointNodeDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    scenario_id: uuid.UUID
    type: str = "EndPoint"


class DecisionTreeDTO(BaseModel):
    tree_node: IssueOutgoingDto | EndPointNodeDto
    children: Optional[List["DecisionTreeDTO"]] = None


# class DecisionTreeDTO2(BaseModel):
#     tree_node: NodeProtocol | EndPointNodeDto
#     children: Optional[List["DecisionTreeDTO2"]] = None