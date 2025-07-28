import uuid
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from typing import Optional

from src.models.issue import Issue
from src.dtos.issue_dtos import (
    IssueMapper,
    IssueOutgoingDto,
    IssueIncomingDto,
)
from src.dtos.node_dtos import (
    NodeMapper,
    NodeIncomingDto,
)
from src.dtos.node_style_dtos import (
    NodeStyleIncomingDto,
)
from src.dtos.decision_dtos import (
    DecisionMapper,
    DecisionIncomingDto,
)
from src.dtos.uncertainty_dtos import (
    UncertaintyMapper,
    UncertaintyIncomingDto,
)
from src.dtos.utility_dtos import (
    UtilityMapper,
    UtilityIncomingDto,
)
from src.dtos.value_metric_dtos import (
    ValueMetricMapper,
    ValueMetricIncomingDto,
)
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.repositories.issue_repository import IssueRepository
from src.repositories.node_repository import NodeRepository
from src.repositories.decision_repository import DecisionRepository
from src.repositories.uncertainty_repository import UncertaintyRepository
from src.repositories.utility_repository import UtilityRepository
from src.repositories.value_metric_repository import ValueMetricRepository 
from src.repositories.user_repository import UserRepository
from src.models.filters.issues_filter import IssueFilter, issue_conditions
from src.services.session_handler import session_handler

class IssueService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine
    
    def _extract_related_entities(self, dtos: list[IssueIncomingDto]) -> tuple[list[IssueIncomingDto], list[NodeIncomingDto], list[Optional[DecisionIncomingDto]], list[Optional[UncertaintyIncomingDto]], list[Optional[UtilityIncomingDto]], list[Optional[ValueMetricIncomingDto]]]:
        nodes: list[NodeIncomingDto]=[]
        decisions: list[Optional[DecisionIncomingDto]]=[]
        uncertainties: list[Optional[UncertaintyIncomingDto]]=[]
        utilities: list[Optional[UtilityIncomingDto]] = []
        value_metrics: list[Optional[ValueMetricIncomingDto]] = []
        for dto in dtos:
            if dto.node:
                nodes.append(dto.node)
            else:
                node_id = uuid.uuid4()
                nodes.append(NodeIncomingDto(id=node_id, scenario_id=dto.scenario_id, issue_id=dto.id, node_style=NodeStyleIncomingDto(node_id=node_id)))

            decisions.append(dto.decision)
            uncertainties.append(dto.uncertainty)
            utilities.append(dto.utility)
            value_metrics.append(dto.value_metric)
            dto.node=None
            dto.decision=None
            dto.uncertainty=None
            dto.utility=None
            dto.value_metric=None
        return dtos, nodes, decisions, uncertainties, utilities, value_metrics
    
    async def _create_related_entities(self, session: AsyncSession, entity: Issue, node_dto: NodeIncomingDto, decision_dto: Optional[DecisionIncomingDto], uncertainty_dto: Optional[UncertaintyIncomingDto], utility_dto: Optional[UtilityIncomingDto], value_metric_dto: Optional[ValueMetricIncomingDto]):
        node_dto.issue_id=entity.id
        node=(await NodeRepository(session).create_single(NodeMapper.to_entity(node_dto)))
        entity.node=node
        if decision_dto:
            decision_dto.issue_id=entity.id
            decision=(await DecisionRepository(session).create_single(DecisionMapper.to_entity(decision_dto)))
            entity.decision=decision
        if uncertainty_dto:
            uncertainty_dto.issue_id=entity.id
            uncertainty=(await UncertaintyRepository(session).create_single(UncertaintyMapper.to_entity(uncertainty_dto)))
            entity.uncertainty=uncertainty
        if utility_dto:
            utility_dto.issue_id=entity.id
            utility=(await UtilityRepository(session).create_single(UtilityMapper.to_entity(utility_dto)))
            entity.utility=utility
        if value_metric_dto:
            value_metric_dto.issue_id=entity.id
            value_metric=(await ValueMetricRepository(session).create_single(ValueMetricMapper.to_entity(value_metric_dto)))
            entity.value_metric=value_metric
        return entity

    async def create(self, dtos: list[IssueIncomingDto], user_dto: UserIncomingDto) -> list[IssueOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            # remove node dto to create later
            dtos, node_dtos, decision_dtos, uncertainty_dtos, utility_dtos, value_metric_dtos = self._extract_related_entities(dtos)
            entities: list[Issue] = await IssueRepository(session).create(IssueMapper.to_entities(dtos, user.id))
            # get the dtos while the entities are still connected to the session
            for entity, node_dto, decision_dto, uncertainty_dto, utility_dto, value_metric_dto in zip(entities, node_dtos, decision_dtos, uncertainty_dtos, utility_dtos, value_metric_dtos):
                entity= await self._create_related_entities(session, entity, node_dto, decision_dto, uncertainty_dto, utility_dto, value_metric_dto)
            result: list[IssueOutgoingDto] = IssueMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[IssueIncomingDto], user_dto: UserIncomingDto) -> list[IssueOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            entities: list[Issue] = await IssueRepository(session).update(IssueMapper.to_entities(dtos, user.id))
            # get the dtos while the entities are still connected to the session
            result: list[IssueOutgoingDto] = IssueMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[uuid.UUID]):
        async with session_handler(self.engine) as session:
            await IssueRepository(session).delete(ids)
    
    async def get(self, ids: list[uuid.UUID]) -> list[IssueOutgoingDto]:
        async with session_handler(self.engine) as session:
            issues: list[Issue] = await IssueRepository(session).get(ids)
            result=IssueMapper.to_outgoing_dtos(issues)
        return result
    
    async def get_all(self, filter: Optional[IssueFilter]=None, odata_query: Optional[str]=None) -> list[IssueOutgoingDto]:
        async with session_handler(self.engine) as session:
            model_filter=IssueFilter.combine_conditions(issue_conditions(filter)) if filter else None
            issues: list[Issue] = await IssueRepository(session).get_all(model_filter=model_filter, odata_query=odata_query)
            result=IssueMapper.to_outgoing_dtos(issues)
        return result
