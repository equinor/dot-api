import uuid
from src.models.utility import Utility
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class UtilityRepository(BaseRepository[Utility, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Utility, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[Utility]) -> list[Utility]:
        entities_to_update=await self.get([utility.id for utility in entities])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.values=entity.values
            if entity.issue_id:
                entity_to_update=entity.issue_id

        await self.session.flush()
        return entities_to_update
