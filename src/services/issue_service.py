from sqlalchemy.ext.asyncio import AsyncEngine
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
from src.dtos.decision_dtos import (
    DecisionMapper,
    DecisionIncomingDto,
)
from src.dtos.uncertainty_dtos import (
    UncertaintyMapper,
    UncertaintyIncomingDto,
)
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.repositories.issue_repository import IssueRepository
from src.repositories.node_repository import NodeRepository
from src.repositories.decision_repository import DecisionRepository
from src.repositories.uncertainty_repository import UncertaintyRepository
from src.repositories.user_repository import UserRepository
from src.services.session_handler import session_handler

class IssueService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine
    
    def _extract_related_entities(self, dtos: list[IssueIncomingDto]) -> tuple[list[IssueIncomingDto], list[NodeIncomingDto], list[Optional[DecisionIncomingDto]], list[Optional[UncertaintyIncomingDto]]]:
        nodes: list[NodeIncomingDto]=[]
        decisions: list[Optional[DecisionIncomingDto]]=[]
        uncertainties: list[Optional[UncertaintyIncomingDto]]=[]
        for dto in dtos:
            if dto.node:
                nodes.append(dto.node)
            else:
                # issue id is set later
                nodes.append(NodeIncomingDto(scenario_id=dto.scenario_id, issue_id=0, id=None))

            decisions.append(dto.decision)
            uncertainties.append(dto.uncertainty)
            dto.node=None
            dto.decision=None
            dto.uncertainty=None
        return dtos, nodes, decisions, uncertainties

    async def create(self, dtos: list[IssueIncomingDto], user_dto: UserIncomingDto) -> list[IssueOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            # remove node dto to create later
            dtos, node_dtos, decision_dtos, uncertainty_dtos = self._extract_related_entities(dtos)
            entities: list[Issue] = await IssueRepository(session).create(IssueMapper.to_entities(dtos, user.id))
            # get the dtos while the entities are still connected to the session
            for entity, node_dto, decision_dto, uncertainty_dto in zip(entities, node_dtos, decision_dtos, uncertainty_dtos):
                node_dto.issue_id=entity.id
                node=(await NodeRepository(session).create(NodeMapper.to_entity(node_dto)))[0]
                entity.node=node
                if decision_dto:
                    decision=(await DecisionRepository(session).create(DecisionMapper.to_entity(decision_dto)))[0]
                    entity.decision=decision
                if uncertainty_dto:
                    uncertainty=(await UncertaintyRepository(session).create(UncertaintyMapper.to_entity(uncertainty_dto)))[0]
                    entity.uncertainty=uncertainty
            result: list[IssueOutgoingDto] = IssueMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[IssueIncomingDto], user_dto: UserIncomingDto) -> list[IssueOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            entities: list[Issue] = await IssueRepository(session).update(IssueMapper.to_entities(dtos, user.id))
            # get the dtos while the entities are still connected to the session
            result: list[IssueOutgoingDto] = IssueMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[int]):
        async with session_handler(self.engine) as session:
            await IssueRepository(session).delete(ids)
    
    async def get(self, ids: list[int]) -> list[IssueOutgoingDto]:
        async with session_handler(self.engine) as session:
            issues: list[Issue] = await IssueRepository(session).get(ids)
            result=IssueMapper.to_outgoing_dtos(issues)
        return result
    
    async def get_all(self) -> list[IssueOutgoingDto]:
        async with session_handler(self.engine) as session:
            issues: list[Issue] = await IssueRepository(session).get_all()
            result=IssueMapper.to_outgoing_dtos(issues)
        return result
    