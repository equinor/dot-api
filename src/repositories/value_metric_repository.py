from src.models.value_metric import ValueMetric
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class ValueMetricRepository(BaseRepository[ValueMetric]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ValueMetric, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[ValueMetric]) -> list[ValueMetric]:
        entities_to_update=await self.get([value_metric.id for value_metric in entities])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.name=entity.name
            if entity.issue_id:
                entity_to_update=entity.issue_id

        await self.session.flush()
        return entities_to_update
    