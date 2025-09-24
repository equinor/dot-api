import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants import Boundary, Type
from src.models.scenario import Scenario
from src.dtos.scenario_dtos import (
    ScenarioMapper,
    ScenarioOutgoingDto,
    ScenarioIncomingDto,
    ScenarioCreateDto,
    PopulatedScenarioDto,
)
from src.dtos.objective_dtos import ObjectiveMapper
from src.dtos.opportunity_dtos import OpportunityMapper
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.models.filters.edge_filter import EdgeFilter
from src.models.filters.issues_filter import IssueFilter
from src.dtos.issue_dtos import IssueOutgoingDto, IssueMapper
from src.dtos.edge_dtos import EdgeOutgoingDto, EdgeMapper

from src.repositories.scenario_repository import ScenarioRepository
from src.repositories.issue_repository import IssueRepository
from src.repositories.edge_repository import EdgeRepository
from src.repositories.user_repository import UserRepository
from src.repositories.objective_repository import ObjectiveRepository
from src.repositories.opportunity_repository import OpportunityRepository
from src.models.filters.scenario_filter import ScenarioFilter


class ScenarioService:
    async def create(
        self,
        session: AsyncSession,
        dtos: list[ScenarioCreateDto],
        user_dto: UserIncomingDto,
    ) -> list[ScenarioOutgoingDto]:
        user = await UserRepository(session).get_or_create(
            UserMapper.to_entity(user_dto)
        )
        # create scenario
        entities: list[Scenario] = await ScenarioRepository(session).create(
            ScenarioMapper.from_create_to_entities(dtos, user.id)
        )

        # create objectives/opportunities
        for entity, dto in zip(entities, dtos):
            objectives = await ObjectiveRepository(session).create(
                ObjectiveMapper.via_scenario_to_entities(
                    dto.objectives, user.id, entity.id
                )
            )
            opportunities = await OpportunityRepository(session).create(
                OpportunityMapper.via_scenario_to_entities(
                    dto.opportunities, user.id, entity.id
                )
            )

            entity.objectives = objectives
            entity.opportunities = opportunities

        # get the dtos while the entities are still connected to the session
        result: list[ScenarioOutgoingDto] = ScenarioMapper.to_outgoing_dtos(entities)
        return result

    async def update(
        self,
        session: AsyncSession,
        dtos: list[ScenarioIncomingDto],
        user_dto: UserIncomingDto,
    ) -> list[ScenarioOutgoingDto]:
        user = await UserRepository(session).get_or_create(
            UserMapper.to_entity(user_dto)
        )
        entities: list[Scenario] = await ScenarioRepository(session).update(
            ScenarioMapper.to_entities(dtos, user.id)
        )
        # get the dtos while the entities are still connected to the session
        result: list[ScenarioOutgoingDto] = ScenarioMapper.to_outgoing_dtos(entities)
        return result

    async def delete(self, session: AsyncSession, ids: list[uuid.UUID]):
        await ScenarioRepository(session).delete(ids)

    async def get(
        self, session: AsyncSession, ids: list[uuid.UUID]
    ) -> list[ScenarioOutgoingDto]:
        scenarios: list[Scenario] = await ScenarioRepository(session).get(ids)
        result = ScenarioMapper.to_outgoing_dtos(scenarios)
        return result

    async def get_populated(
        self, session: AsyncSession, ids: list[uuid.UUID]
    ) -> list[PopulatedScenarioDto]:
        scenarios: list[Scenario] = await ScenarioRepository(session).get(ids)
        result = ScenarioMapper.to_populated_dtos(scenarios)
        return result

    async def get_all(
        self,
        session: AsyncSession,
        filter: Optional[ScenarioFilter] = None,
        odata_query: Optional[str] = None,
    ) -> list[ScenarioOutgoingDto]:
        model_filter = filter.construct_filters() if filter else []
        scenarios: list[Scenario] = await ScenarioRepository(session).get_all(
            model_filter=model_filter, odata_query=odata_query
        )
        result = ScenarioMapper.to_outgoing_dtos(scenarios)
        return result

    async def get_all_populated(
        self,
        session: AsyncSession,
        filter: Optional[ScenarioFilter] = None,
        odata_query: Optional[str] = None,
    ) -> list[PopulatedScenarioDto]:
        model_filter = filter.construct_filters() if filter else []
        scenarios: list[Scenario] = await ScenarioRepository(session).get_all(
            model_filter=model_filter, odata_query=odata_query
        )
        result = ScenarioMapper.to_populated_dtos(scenarios)
        return result

    async def get_influence_diagram_data(
        self, session: AsyncSession, scenario_id: uuid.UUID
    ) -> tuple[list[IssueOutgoingDto], list[EdgeOutgoingDto]]:
        issue_filter = IssueFilter(
            scenario_ids=[scenario_id],
            boundaries=[Boundary.ON.value, Boundary.IN.value],
            types=[Type.DECISION.value, Type.UNCERTAINTY.value],
        )
        edge_filter = EdgeFilter(
            scenario_ids=[scenario_id],
            issue_boundaries=[Boundary.ON.value, Boundary.IN.value],
            issue_types=[Type.DECISION.value, Type.UNCERTAINTY.value],
        )

        issues_entities = await IssueRepository(session).get_all(
            model_filter=issue_filter.construct_filters()
        )
        edges_entities = await EdgeRepository(session).get_all(
            model_filter=edge_filter.construct_filters()
        )

        issue_dtos = IssueMapper.to_outgoing_dtos(issues_entities)
        edge_dtos = EdgeMapper.to_outgoing_dtos(edges_entities)

        return issue_dtos, edge_dtos
