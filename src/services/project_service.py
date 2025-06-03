from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models import (
    Project,
    User,
)
from src.dtos.project_dtos import (
    ProjectMapper,
    ProjectIncomingDto,
    ProjectOutgoingDto,
    ProjectCreateDto,
)
from src.dtos.user_dtos import (
    UserMapper,
    UserIncomingDto,
)
from src.dtos.objective_dtos import (
    ObjectiveMapper,
    ObjectiveViaScenarioDto
)
from src.dtos.opportunity_dtos import (
    OpportunityMapper,
    OpportunityViaProjectDto,
)
from src.dtos.scenario_dtos import (
    ScenarioMapper,
    ScenarioCreateViaProjectDto,
)
from src.repositories.project_repository import ProjectRepository
from src.repositories.user_repository import UserRepository
from src.repositories.scenario_repository import ScenarioRepository
from src.repositories.opportunity_repository import OpportunityRepository
from src.repositories.objective_repository import ObjectiveRepository
from src.services.session_handler import session_handler

class ProjectService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def _create_scenarios_for_project(self, session: AsyncSession, scenario_dtos: list[ScenarioCreateViaProjectDto], user: User, project_id: int):
        scenarios = await ScenarioRepository(session).create(ScenarioMapper.from_create_via_project_to_entities(scenario_dtos, user.id, project_id))
        for scenario_dto, scenario in zip(scenario_dtos, scenarios):
            objectives, opportunities = await self._create_opportunities_and_objectives_for_scenario(session, scenario_dto.objectives, scenario_dto.opportunities, user, scenario.id)
            scenario.objectives, scenario.opportunities = objectives, opportunities
        return scenarios

    async def _create_opportunities_and_objectives_for_scenario(self, session: AsyncSession, objective_dtos: list[ObjectiveViaScenarioDto], opportunities_dtos: list[OpportunityViaProjectDto], user: User, scenario_id: int):
        objectives=await ObjectiveRepository(session).create(ObjectiveMapper.via_scenario_to_entities(objective_dtos, user.id, scenario_id))
        opportunities=await OpportunityRepository(session).create(OpportunityMapper.via_project_to_entities(opportunities_dtos, user.id, scenario_id))
        return objectives, opportunities

    async def create(self, dtos: list[ProjectCreateDto], user_dto: UserIncomingDto) -> list[ProjectOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            entities: list[Project] = await ProjectRepository(session).create(ProjectMapper.from_create_to_entities(dtos, user.id))

            for entity, dto in zip(entities, dtos):
                scenarios=await self._create_scenarios_for_project(session, dto.scenarios, user, entity.id)
                entity.scenarios=scenarios

            # get the dtos while the entities are still connected to the session
            result: list[ProjectOutgoingDto] = ProjectMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[ProjectIncomingDto], user_dto: UserIncomingDto) -> list[ProjectOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            entities: list[Project] = await ProjectRepository(session).update(ProjectMapper.to_entities(dtos, user.id))
            # get the dtos while the entities are still connected to the session
            result: list[ProjectOutgoingDto] = ProjectMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[int]):
        async with session_handler(self.engine) as session:
            await ProjectRepository(session).delete(ids)
    
    async def get(self, ids: list[int]) -> list[ProjectOutgoingDto]:
        async with session_handler(self.engine) as session:
            projects: list[Project] = await ProjectRepository(session).get(ids)
            result=ProjectMapper.to_outgoing_dtos(projects)
        return result
    
    async def get_all(self) -> list[ProjectOutgoingDto]:
        async with session_handler(self.engine) as session:
            projects: list[Project] = await ProjectRepository(session).get_all()
            result = ProjectMapper.to_outgoing_dtos(projects)
        return result
