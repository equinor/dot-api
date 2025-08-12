import uuid
from src.models.scenario import Scenario
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class ScenarioRepository(BaseRepository[Scenario, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Scenario, query_extension_method=QueryExtensions.load_scenario_with_relationships)
    
    async def update(self, entities: list[Scenario]) -> list[Scenario]:
        entities_to_update=await self.get([decision.id for decision in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.name=entity.name
            entity_to_update.project_id=entity.project_id
            entity_to_update.objectives=entity.objectives
            entity_to_update.opportunities=entity.opportunities
            
        await self.session.flush()
        return entities_to_update
