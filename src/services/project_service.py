import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from src.constants import ProjectRoleType
from src.dtos.project_roles_dtos import ProjectRoleCreateDto, ProjectRoleMapper
from src.models.project_role import ProjectRole
from src.repositories.project_role_repository import ProjectRoleRepository
from src.models import (
    Project,
    User,
)
from src.dtos.project_dtos import (
    ProjectMapper,
    ProjectIncomingDto,
    ProjectOutgoingDto,
    ProjectCreateDto,
    PopulatedProjectDto,
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
from src.repositories.user_repository import UserRepository
from src.repositories.opportunity_repository import OpportunityRepository
from src.repositories.objective_repository import ObjectiveRepository
from src.models.filters.project_filter import ProjectFilter
from src.services.session_handler import session_handler

class ProjectService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def _create_scenarios_for_project(self, session: AsyncSession, scenario_dtos: list[ScenarioCreateViaProjectDto], user: User, project_id: uuid.UUID):
        scenarios = await ScenarioRepository(session).create(ScenarioMapper.from_create_via_project_to_entities(scenario_dtos, user.id, project_id))
        for scenario_dto, scenario in zip(scenario_dtos, scenarios):
            objectives, opportunities = await self._create_opportunities_and_objectives_for_scenario(session, scenario_dto.objectives, scenario_dto.opportunities, user, scenario.id)
            scenario.objectives, scenario.opportunities = objectives, opportunities
        return scenarios
    
    async def _create_role_for_project(self, session: AsyncSession, project_role_dtos: list[ProjectRoleCreateDto], user: User, project_id: uuid.UUID):
        project_user_roles = await ProjectRoleRepository(session).create(ProjectRoleMapper.from_create_via_project_to_entities(project_role_dtos, user.id, project_id))
        for project_role in project_user_roles:
            user_info = await UserRepository(session).get([project_role.user_id])
            if user_info:
                project_role.user_name = user_info[0].name
                project_role.azure_id = user_info[0].azure_id
        return project_user_roles

    async def _create_opportunities_and_objectives_for_scenario(self, session: AsyncSession, objective_dtos: list[ObjectiveViaScenarioDto], opportunities_dtos: list[OpportunityViaProjectDto], user: User, scenario_id: uuid.UUID):
        objectives=await ObjectiveRepository(session).create(ObjectiveMapper.via_scenario_to_entities(objective_dtos, user.id, scenario_id))
        opportunities=await OpportunityRepository(session).create(OpportunityMapper.via_scenario_to_entities(opportunities_dtos, user.id, scenario_id))
        return objectives, opportunities

    async def create(self, dtos: list[ProjectCreateDto], user_dto: UserIncomingDto) -> list[ProjectOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            for dto in dtos:
                owner_role = ProjectRoleCreateDto(
                    id=dto.id, # will be overwritten in the loop below
                    user_name=user.name,
                    user_id=user.id,
                    azure_id= user.azure_id,
                    project_id=dto.id, # will be overwritten in the loop below
                    role=ProjectRoleType.OWNER
                )
                dto.users.append(owner_role)

            project_entities: list[Project] = await ProjectRepository(session).create(ProjectMapper.from_create_to_project_entities(dtos, user.id))
            for project_entity, dto in zip(project_entities, dtos):
                if len(dto.users) > 0:
                    project_role_entities: list[ProjectRole] = await self._create_role_for_project(session, dto.users, user, project_entity.id)
                    project_entity.project_role=project_role_entities
                scenarios=await self._create_scenarios_for_project(session, dto.scenarios, user, project_entity.id)
                project_entity.scenarios=scenarios
            result: list[ProjectOutgoingDto] = ProjectMapper.to_outgoing_dtos(project_entities)
        return result
    
    async def update(self, dtos: list[ProjectIncomingDto], user_dto: UserIncomingDto) -> list[ProjectOutgoingDto]:
        async with session_handler(self.engine) as session:
            user=await UserRepository(session).get_or_create(UserMapper.to_entity(user_dto))
            entities_project: list[Project] = await ProjectRepository(session).update(ProjectMapper.to_project_entities(dtos, user.id))
            for entity_project in entities_project:
                for project_role in entity_project.project_role:
                    user_info = await UserRepository(session).get([project_role.user_id])
                    if user_info:
                        project_role.user_name = user_info[0].name
                        project_role.azure_id = user_info[0].azure_id
            result: list[ProjectOutgoingDto] = ProjectMapper.to_outgoing_dtos(entities_project)
        return result

    async def delete(self, ids: list[uuid.UUID], user_dto: UserIncomingDto) -> None:
        async with session_handler(self.engine) as session:
            user_role = await ProjectRoleRepository(session).get_accessible_projects_by_user(azure_id=user_dto.azure_id)
            ids_to_delete = [project_role.project_id for project_role in user_role if project_role.role == ProjectRoleType.OWNER and project_role.project_id in ids]
            await ProjectRepository(session).delete(ids=ids_to_delete)

    async def get(self, ids: list[uuid.UUID]) -> list[ProjectOutgoingDto]:
        async with session_handler(self.engine) as session:
            if not ids:
                return []
            projects: list[Project] = await ProjectRepository(session).get(ids)
            result=ProjectMapper.to_outgoing_dtos(projects)
        return result
        
    async def get_all(self, user_dto: UserIncomingDto, filter: Optional[ProjectFilter]=None, odata_query: Optional[str]=None) -> list[ProjectOutgoingDto]:
        async with session_handler(self.engine) as session:
            user = await UserRepository(session).get_by_azure_id(user_dto.azure_id)
            if not user:
                return []
            if filter is None:
                filter = ProjectFilter()
            
            filter.accessing_user_id = user.id
            project_access_filter = filter.construct_access_conditions()
            
            # Construct model filters
            model_filter = filter.construct_filters() if filter else []
            model_filter.append(project_access_filter)
            
            projects: list[Project] = await ProjectRepository(session).get_all(model_filter=model_filter, odata_query=odata_query)
            for project in projects:
                for project_role in project.project_role:
                        user_info = await UserRepository(session).get([project_role.user_id])
                        if user_info:
                            project_role.user_name = user_info[0].name
                            project_role.azure_id = user_info[0].azure_id
            result = ProjectMapper.to_outgoing_dtos(projects)
        return result

    async def get_populated_projects(self, ids: list[uuid.UUID]) -> list[PopulatedProjectDto]:
        async with session_handler(self.engine) as session:
            projects: list[Project] = await ProjectRepository(session).get(ids)
            result=ProjectMapper.to_populated_dtos(projects)
        return result
    
    async def get_all_populated_projects(self, filter: Optional[ProjectFilter]=None, odata_query: Optional[str]=None) -> list[PopulatedProjectDto]:
        async with session_handler(self.engine) as session:
            model_filter=filter.construct_filters() if filter else []
            projects: list[Project] = await ProjectRepository(session).get_all(model_filter=model_filter, odata_query=odata_query)
            result=ProjectMapper.to_populated_dtos(projects)
        return result