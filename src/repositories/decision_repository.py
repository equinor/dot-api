from src.models.decision import Decision
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class DecisionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Decision]) -> list[Decision]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Decision]:
        return list(
            (await self.session.scalars(select(Decision).where(Decision.id.in_(ids)))).all()
        )
    
    async def get_all(self) -> list[Decision]:
        return list(
            (await self.session.scalars(select(Decision))).all()
        )
    
    async def update(self, entities: list[Decision]) -> list[Decision]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.options=entity.options
            if entity.issue_id:
                enity_to_update=entity.issue_id

        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
