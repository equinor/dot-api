from src.models import Probability
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ProbabilityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Probability]) -> list[Probability]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Probability]:
        return list(
            (await self.session.scalars(select(Probability).where(Probability.id.in_(ids)))).all()
        )
    
    async def get_all(self) -> list[Probability]:
        return list(
            (await self.session.scalars(select(Probability))).all()
        )
    
    async def update(self, entities: list[Probability]) -> list[Probability]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.probabilities=entity.probabilities
            
        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
