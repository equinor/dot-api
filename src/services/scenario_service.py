from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.scenario import Scenario
from src.dtos.scenario_dtos import *
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.repositories.scenario_repository import ScenarioRepository
from src.repositories.user_repository import UserRepository
from src.repositories.objective_repository import ObjectiveRepository
from src.repositories.opportunity_repository import OpportunityRepository

class ScenarioService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[ScenarioCreateDto], user_dto: UserIncomingDto) -> list[ScenarioOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                # create scenario
                entities: list[Scenario] = await ScenarioRepository(session).create(ScenarioMapper.from_create_to_entities(dtos, user.id))

                # create objectives/opportunities
                for entity, dto in zip(entities, dtos):
                    objectives=await ObjectiveRepository(session).create(ObjectiveMapper.via_scenario_to_entities(dto.objectives, user.id, entity.id))
                    opportunities=await OpportunityRepository(session).create(OpportunityMapper.via_project_to_entities(dto.opportunities, user.id, entity.id))

                    entity.objectives=objectives
                    entity.opportunities=opportunities

                # get the dtos while the entities are still connected to the session
                result: list[ScenarioOutgoingDto] = ScenarioMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def update(self, dtos: list[ScenarioIncomingDto], user_dto: UserIncomingDto) -> list[ScenarioOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
                entities: list[Scenario] = await ScenarioRepository(session).update(ScenarioMapper.to_entities(dtos, user.id))
                # get the dtos while the entities are still connected to the session
                result: list[ScenarioOutgoingDto] = ScenarioMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def delete(self, ids: list[int]):
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                await ScenarioRepository(session).delete(ids)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get(self, ids: list[int]) -> list[ScenarioOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            scenarios: list[Scenario] = await ScenarioRepository(session).get(ids)
            result=ScenarioMapper.to_outgoing_dtos(scenarios)
        return result
    
    async def get_all(self) -> list[ScenarioOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            scenarios: list[Scenario] = await ScenarioRepository(session).get_all()
            result=ScenarioMapper.to_outgoing_dtos(scenarios)
        return result
