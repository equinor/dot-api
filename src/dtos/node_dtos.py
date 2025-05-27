from pydantic import BaseModel
from typing import Optional
from src.models.node import (
    Node
)
from src.dtos.user_dtos import *
from src.dtos.decision_dtos import *
from src.dtos.probability_dtos import *
from src.dtos.node_dtos import *

class NodeDto(BaseModel):
    graph_id: int
    type: str

class NodeIncomingDto(NodeDto):
    id: Optional[int]
    decision: Optional[DecisionIncomingDto]
    probability: Optional[ProbabilityIncomingDto]

class NodeOutgoingDto(NodeDto):
    id: int
    decision: Optional[DecisionOutgoingDto]
    probability: Optional[ProbabilityOutgoingDto]

class NodeMapper:
    @staticmethod
    def to_outgoing_dto(entity: Node) -> NodeOutgoingDto:
        return NodeOutgoingDto(
            id=entity.id,
            graph_id=entity.graph_id,
            type=entity.type,
            decision=DecisionMapper.to_outgoing_dto(entity.decision) if entity.decision else None,
            probability=ProbabilityMapper.to_outgoing_dto(entity.probability) if entity.probability else None
        )

    @staticmethod
    def to_entity(dto: NodeIncomingDto, user_id: int) -> Node:
        # decision and probability ids are not assigned here as the node controls the decisions and probabilities
        return Node(
            id=dto.id,
            graph_id=dto.graph_id,
            type=dto.type,
            user_id=user_id,
            decision=DecisionMapper.to_entity(dto.decision) if dto.decision else None,
            probability=
            ProbabilityMapper.to_entity(dto.probability) if dto.probability else None
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Node]) -> list[NodeOutgoingDto]:
        return [NodeMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[NodeIncomingDto], user_id: int) -> list[Node]:
        return [NodeMapper.to_entity(dto, user_id) for dto in dtos]