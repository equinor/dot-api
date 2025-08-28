import uuid
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Annotated
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
from src.dtos.utility_dtos import (
    UtilityMapper,
    UtilityIncomingDto,
    UtilityOutgoingDto
)
from src.dtos.value_metric_dtos import (
    ValueMetricMapper,
    ValueMetricOutgoingDto,
    ValueMetricIncomingDto,
)
from src.dtos.node_dtos import (
    NodeMapper,
    NodeIncomingDto,
    NodeOutgoingDto,
    NodeViaIssueOutgoingDto,
)
from src.constants import DatabaseConstants

class IssueDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    scenario_id: uuid.UUID
    name: Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)] = ""
    description: Annotated[str, Field(max_length=DatabaseConstants.MAX_LONG_STRING_LENGTH.value)] = ""
    order: int

class IssueIncomingDto(IssueDto):
    model_config=ConfigDict(use_enum_values=True)

    type: Type = Type.UNDECIDED
    boundary: Boundary = Boundary.OUT
    node: Optional[NodeIncomingDto]
    decision: Optional[DecisionIncomingDto]
    uncertainty: Optional[UncertaintyIncomingDto]
    utility: Optional[UtilityIncomingDto]
    value_metric: Optional[ValueMetricIncomingDto]

class IssueOutgoingDto(IssueDto):
    type: str
    boundary: str
    node: NodeViaIssueOutgoingDto
    decision: Optional[DecisionOutgoingDto]
    uncertainty: Optional[UncertaintyOutgoingDto]
    utility: Optional[UtilityOutgoingDto]
    value_metric: Optional[ValueMetricOutgoingDto]

class IssueViaNodeOutgoingDto(IssueDto):
    type: str
    boundary: str
    decision: Optional[DecisionOutgoingDto]
    uncertainty: Optional[UncertaintyOutgoingDto]
    utility: Optional[UtilityOutgoingDto]
    value_metric: Optional[ValueMetricOutgoingDto]

class IssueMapper:
    @staticmethod
    def to_outgoing_dto(entity: Issue) -> IssueOutgoingDto:
        return IssueOutgoingDto(
            id=entity.id,
            scenario_id=entity.scenario_id,
            type=entity.type,
            boundary=entity.boundary,
            name=entity.name,
            description=entity.description,
            order=entity.order,
            node=NodeMapper.to_outgoing_dto_via_issue(entity.node),
            decision=DecisionMapper.to_outgoing_dto(entity.decision) if entity.decision else None,
            uncertainty=UncertaintyMapper.to_outgoing_dto(entity.uncertainty) if entity.uncertainty else None,
            utility=UtilityMapper.to_outgoing_dto(entity.utility) if entity.utility else None,
            value_metric=ValueMetricMapper.to_outgoing_dto(entity.value_metric) if entity.value_metric else None,
        )

    @staticmethod
    def to_outgoing_dto_via_node(entity: Issue) -> IssueViaNodeOutgoingDto:
        return IssueViaNodeOutgoingDto(
            id=entity.id,
            scenario_id=entity.scenario_id,
            type=entity.type,
            boundary=entity.boundary,
            name=entity.name,
            description=entity.description,
            order=entity.order,
            decision=DecisionMapper.to_outgoing_dto(entity.decision) if entity.decision else None,
            uncertainty=UncertaintyMapper.to_outgoing_dto(entity.uncertainty) if entity.uncertainty else None,
            utility=UtilityMapper.to_outgoing_dto(entity.utility) if entity.utility else None,
            value_metric=ValueMetricMapper.to_outgoing_dto(entity.value_metric) if entity.value_metric else None,
        )

    @staticmethod
    def to_entity(dto: IssueIncomingDto, user_id: int) -> Issue:
        # decision and uncertainty ids are not assigned here as the issue controls the decisions and uncertainties
        return Issue(
            id=dto.id,
            scenario_id=dto.scenario_id,
            type=dto.type,
            boundary=dto.boundary,
            order=dto.order,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
            node=NodeMapper.to_entity(dto.node) if dto.node else None,
            decision=DecisionMapper.to_entity(dto.decision) if dto.decision else None,
            uncertainty=UncertaintyMapper.to_entity(dto.uncertainty) if dto.uncertainty else None,
            utility=UtilityMapper.to_entity(dto.utility) if dto.utility else None,
            value_metric=ValueMetricMapper.to_entity(dto.value_metric) if dto.value_metric else None,
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[Issue]) -> list[IssueOutgoingDto]:
        return [IssueMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[IssueIncomingDto], user_id: int) -> list[Issue]:
        return [IssueMapper.to_entity(dto, user_id) for dto in dtos]

NodeOutgoingDto.model_rebuild()
