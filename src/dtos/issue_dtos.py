from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.constants import (
    Type, 
    Boundary
)
from src.models.issue import (
    Issue
)
from src.dtos.decision_dtos import (
    DecisionMapper,
    DecisionIncomingDto,
    DecisionOutgoingDto,
)
from src.dtos.uncertainty_dtos import (
    UncertaintyMapper,
    UncertaintyIncomingDto,
    UncertaintyOutgoingDto,
)
from src.dtos.node_dtos import (
    NodeMapper,
    NodeIncomingDto,
    NodeOutgoingDto,
    NodeViaIssueOutgoingDto,
)

class IssueDto(BaseModel):
    scenario_id: int

class IssueIncomingDto(IssueDto):
    model_config=ConfigDict(use_enum_values=True)

    id: Optional[int]
    type: Type = Type.UNDECIDED
    boundary: Boundary = Boundary.OUT
    node: Optional[NodeIncomingDto]
    decision: Optional[DecisionIncomingDto]
    uncertainty: Optional[UncertaintyIncomingDto]

class IssueOutgoingDto(IssueDto):
    id: int
    type: str
    boundary: str
    node: NodeViaIssueOutgoingDto
    decision: Optional[DecisionOutgoingDto]
    uncertainty: Optional[UncertaintyOutgoingDto]

class IssueViaNodeOutgoingDto(IssueDto):
    id: int
    type: str
    boundary: str
    decision: Optional[DecisionOutgoingDto]
    uncertainty: Optional[UncertaintyOutgoingDto]

class IssueMapper:
    @staticmethod
    def to_outgoing_dto(entity: Issue) -> IssueOutgoingDto:
        return IssueOutgoingDto(
            id=entity.id,
            scenario_id=entity.scenario_id,
            type=entity.type,
            boundary=entity.boundary,
            node=NodeMapper.to_outgoing_dto_via_issue(entity.node),
            decision=DecisionMapper.to_outgoing_dto(entity.decision) if entity.decision else None,
            uncertainty=UncertaintyMapper.to_outgoing_dto(entity.uncertainty) if entity.uncertainty else None,
        )

    @staticmethod
    def to_outgoing_dto_via_node(entity: Issue) -> IssueViaNodeOutgoingDto:
        return IssueViaNodeOutgoingDto(
            id=entity.id,
            scenario_id=entity.scenario_id,
            type=entity.type,
            boundary=entity.boundary,
            decision=DecisionMapper.to_outgoing_dto(entity.decision) if entity.decision else None,
            uncertainty=UncertaintyMapper.to_outgoing_dto(entity.uncertainty) if entity.uncertainty else None,
        )

    @staticmethod
    def to_entity(dto: IssueIncomingDto, user_id: int) -> Issue:
        # decision and uncertainty ids are not assigned here as the issue controls the decisions and uncertainties
        return Issue(
            id=dto.id,
            scenario_id=dto.scenario_id,
            type=dto.type,
            boundary=dto.boundary,
            user_id=user_id,
            node=NodeMapper.to_entity(dto.node) if dto.node else None,
            decision=DecisionMapper.to_entity(dto.decision) if dto.decision else None,
            uncertainty=UncertaintyMapper.to_entity(dto.uncertainty) if dto.uncertainty else None,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Issue]) -> list[IssueOutgoingDto]:
        return [IssueMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[IssueIncomingDto], user_id: int) -> list[Issue]:
        return [IssueMapper.to_entity(dto, user_id) for dto in dtos]
    
NodeOutgoingDto.model_rebuild()