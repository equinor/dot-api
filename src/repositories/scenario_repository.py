from src.models.scenario import Scenario
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ScenarioRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Scenario]) -> list[Scenario]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Scenario]:
        query=select(Scenario).where(Scenario.id.in_(ids)).options(
            *QueryExtensions.load_scenario_with_relationships()
        )
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def get_all(self) -> list[Scenario]:
        query=select(Scenario).options(
            *QueryExtensions.load_scenario_with_relationships()
        )
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def update(self, entities: list[Scenario]) -> list[Scenario]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.name=entity.name
            enity_to_update.project_id=entity.project_id
            enity_to_update.objectives=entity.objectives
            enity_to_update.opportunities=entity.opportunities
            
        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
