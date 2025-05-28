from pydantic import BaseModel
from typing import Optional
from src.models.issue import (
    Issue
)
from src.dtos.user_dtos import *
from src.dtos.decision_dtos import *
from src.dtos.probability_dtos import *
from src.dtos.node_dtos import *

class IssueDto(BaseModel):
    scenario_id: int
    node_id: int
    type: str
    boundary: str

class IssueIncomingDto(IssueDto):
    id: Optional[int]
    node: Optional[NodeIncomingDto]
    decision: Optional[DecisionIncomingDto]
    probability: Optional[ProbabilityIncomingDto]

class IssueOutgoingDto(IssueDto):
    id: int
    node: NodeViaIssueOutgoingDto
    decision: Optional[DecisionOutgoingDto]
    probability: Optional[ProbabilityOutgoingDto]

class IssueViaNodeOutgoingDto(IssueDto):
    id: int
    decision: Optional[DecisionOutgoingDto]
    probability: Optional[ProbabilityOutgoingDto]

class IssueMapper:
    @staticmethod
    def to_outgoing_dto(entity: Issue) -> IssueOutgoingDto:
        return IssueOutgoingDto(
            id=entity.id,
            scenario_id=entity.scenario_id,
            node_id=entity.node_id,
            type=entity.type,
            boundary=entity.boundary,
            node=NodeMapper.to_outgoing_dto_via_issue(entity.node),
            decision=DecisionMapper.to_outgoing_dto(entity.decision) if entity.decision else None,
            probability=ProbabilityMapper.to_outgoing_dto(entity.probability) if entity.probability else None,
        )

    @staticmethod
    def to_outgoing_dto_via_node(entity: Issue) -> IssueViaNodeOutgoingDto:
        return IssueViaNodeOutgoingDto(
            id=entity.id,
            scenario_id=entity.scenario_id,
            node_id=entity.node_id,
            type=entity.type,
            boundary=entity.boundary,
            decision=DecisionMapper.to_outgoing_dto(entity.decision) if entity.decision else None,
            probability=ProbabilityMapper.to_outgoing_dto(entity.probability) if entity.probability else None,
        )

    @staticmethod
    def to_entity(dto: IssueIncomingDto, user_id: int) -> Issue:
        # decision and probability ids are not assigned here as the issue controls the decisions and probabilities
        return Issue(
            id=dto.id,
            scenario_id=dto.scenario_id,
            node_id=dto.node_id,
            type=dto.type,
            boundary=dto.boundary,
            user_id=user_id,
            node=NodeMapper.to_entity(dto.node) if dto.node else None,
            decision=DecisionMapper.to_entity(dto.decision) if dto.decision else None,
            probability=ProbabilityMapper.to_entity(dto.probability) if dto.probability else None,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Issue]) -> list[IssueOutgoingDto]:
        return [IssueMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[IssueIncomingDto], user_id: int) -> list[Issue]:
        return [IssueMapper.to_entity(dto, user_id) for dto in dtos]
    
NodeOutgoingDto.model_rebuild()