from src.models.value_metric import ValueMetric
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ValueMetricRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[ValueMetric]) -> list[ValueMetric]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[ValueMetric]:
        return list(
            (await self.session.scalars(select(ValueMetric).where(ValueMetric.id.in_(ids)))).all()
        )
    
    async def get_all(self) -> list[ValueMetric]:
        return list(
            (await self.session.scalars(select(ValueMetric))).all()
        )
    
    async def update(self, entities: list[ValueMetric]) -> list[ValueMetric]:
        entities_to_update=await self.get([value_metric.id for value_metric in entities])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.name=entity.name
            if entity.issue_id:
                entity_to_update=entity.issue_id

        await self.session.flush()
        return entities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
