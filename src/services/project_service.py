from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models import Project
from src.dtos.project_dtos import (
    ProjectIncomingDto, 
    ProjectOutgoingDto, 
    ProjectMapper
)
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.repositories.project_repository import ProjectRepository
from src.repositories.user_repository import UserRepository

class ProjectService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[ProjectIncomingDto], user_dto: UserIncomingDto) -> list[ProjectOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                entities: list[Project] = await ProjectRepository(session).create(ProjectMapper.to_entities(dtos, user.id))
                # get the dtos while the entities are still connected to the session
                result: list[ProjectOutgoingDto] = ProjectMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def update(self, dtos: list[ProjectIncomingDto], user_dto: UserIncomingDto) -> list[ProjectOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                entities: list[Project] = await ProjectRepository(session).update(ProjectMapper.to_entities(dtos, user.id))
                # get the dtos while the entities are still connected to the session
                result: list[ProjectOutgoingDto] = ProjectMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def delete(self, ids: list[int]):
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                await ProjectRepository(session).delete(ids)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get(self, ids: list[int]) -> list[ProjectOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            projects: list[Project] = await ProjectRepository(session).get(ids)
        return ProjectMapper.to_outgoing_dtos(projects)
    
    async def get_all(self) -> list[ProjectOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            projects: list[Project] = await ProjectRepository(session).get_all()
        return ProjectMapper.to_outgoing_dtos(projects)
