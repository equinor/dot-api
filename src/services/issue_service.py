from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.issue import Issue
from src.dtos.issue_dtos import *
from src.dtos.node_dtos import *
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.repositories.issue_repository import IssueRepository
from src.repositories.node_repository import NodeRepository
from src.repositories.user_repository import UserRepository

class IssueService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine
    
    def _extract_nodes(self, dtos: list[IssueIncomingDto]) -> tuple[list[IssueIncomingDto], list[NodeIncomingDto]]:
        nodes: list[NodeIncomingDto]=[]
        for dto in dtos:
            if dto.node:
                nodes.append(dto.node)
            else:
                # issue id is set later
                nodes.append(NodeIncomingDto(scenario_id=dto.scenario_id, issue_id=0, id=None))
            dto.node=None
        return dtos, nodes

    async def create(self, dtos: list[IssueIncomingDto], user_dto: UserIncomingDto) -> list[IssueOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                # remove node dto to create later
                dtos, node_dtos = self._extract_nodes(dtos)
                entities: list[Issue] = await IssueRepository(session).create(IssueMapper.to_entities(dtos, user.id))
                # get the dtos while the entities are still connected to the session
                for entity, node_dto in zip(entities, node_dtos):
                    node_dto.issue_id=entity.id
                    node=(await NodeRepository(session).create(NodeMapper.to_entity(node_dto)))[0]
                    entity.node=node
                result: list[IssueOutgoingDto] = IssueMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def update(self, dtos: list[IssueIncomingDto], user_dto: UserIncomingDto) -> list[IssueOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                entities: list[Issue] = await IssueRepository(session).update(IssueMapper.to_entities(dtos, user.id))
                # get the dtos while the entities are still connected to the session
                result: list[IssueOutgoingDto] = IssueMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def delete(self, ids: list[int]):
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                await IssueRepository(session).delete(ids)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get(self, ids: list[int]) -> list[IssueOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            issues: list[Issue] = await IssueRepository(session).get(ids)
            result=IssueMapper.to_outgoing_dtos(issues)
        return result
    
    async def get_all(self) -> list[IssueOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            issues: list[Issue] = await IssueRepository(session).get_all()
            result=IssueMapper.to_outgoing_dtos(issues)
        return result
    