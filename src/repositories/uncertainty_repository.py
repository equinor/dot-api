from src.models.uncertainty import Uncertainty
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class UncertaintyRepository(BaseRepository[Uncertainty]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Uncertainty, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[Uncertainty]) -> list[Uncertainty]:
        entities_to_update=await self.get([decision.id for decision in entities])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.probabilities=entity.probabilities
            if entity.issue_id:
                entity_to_update=entity.issue_id
            
        await self.session.flush()
        return entities_to_update
    