from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models import Project
from src.dtos.project_dtos import *
from src.dtos.user_dtos import *
from src.dtos.objective_dtos import *
from src.dtos.opportunity_dtos import *
from src.repositories.project_repository import ProjectRepository
from src.repositories.user_repository import UserRepository
from src.repositories.objective_repository import ObjectiveRepository
from src.repositories.opportunity_repository import OpportunityRepository

class ProjectService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[ProjectCreateDto], user_dto: UserIncomingDto) -> list[ProjectOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                # create projects
                entities: list[Project] = await ProjectRepository(session).create(ProjectMapper.from_create_to_entities(dtos, user.id))

                # create objectives/opportunities
                for n, dto in enumerate(dtos):
                    objectives=await ObjectiveRepository(session).create(ObjectiveMapper.via_project_to_entities(dto.Objectives, user.id, entities[n].id))
                    opportunities=await OpportunityRepository(session).create(OpportunityMapper.via_project_to_entities(dto.Opportunities, user.id, entities[n].id))

                    entities[n].objectives=objectives
                    entities[n].opportunities=opportunities

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
            result=ProjectMapper.to_outgoing_dtos(projects)
        return result
    
    async def get_all(self) -> list[ProjectOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            projects: list[Project] = await ProjectRepository(session).get_all()
            result = ProjectMapper.to_outgoing_dtos(projects)
        return result
