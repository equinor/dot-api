from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from src.models.node import (
    Node
)
from src.dtos.user_dtos import *
from src.dtos.decision_dtos import *
from src.dtos.probability_dtos import *
from src.dtos.node_dtos import *

if TYPE_CHECKING:
    from src.dtos.issue_dtos import (
        IssueViaNodeOutgoingDto
    )

class NodeDto(BaseModel):
    scenario_id: int
    issue_id: int
    name: str = Field(default="")

class NodeIncomingDto(NodeDto):
    id: Optional[int]    

class NodeOutgoingDto(NodeDto):
    id: int
    issue: "IssueViaNodeOutgoingDto"

class NodeViaIssueOutgoingDto(NodeDto):
    id: int

class NodeMapper:
    @staticmethod
    def to_outgoing_dto(entity: Node) -> NodeOutgoingDto:
        from src.dtos.issue_dtos import IssueMapper
        return NodeOutgoingDto(
            id=entity.id,
            issue_id=entity.issue_id,
            scenario_id=entity.scenario_id,
            name=entity.name,
            issue=IssueMapper.to_outgoing_dto_via_node(entity.issue)
        )
    
    @staticmethod
    def to_outgoing_dto_via_issue(entity: Node) -> NodeViaIssueOutgoingDto:
        return NodeViaIssueOutgoingDto(
            id=entity.id,
            issue_id=entity.issue_id,
            scenario_id=entity.scenario_id,
            name=entity.name,
        )

    @staticmethod
    def to_entity(dto: NodeIncomingDto) -> Node:
        return Node(
            id=dto.id,
            issue_id=dto.issue_id,
            scenario_id=dto.scenario_id,
            name=dto.name,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Node]) -> list[NodeOutgoingDto]:
        return [NodeMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[NodeIncomingDto]) -> list[Node]:
        return [NodeMapper.to_entity(dto) for dto in dtos]