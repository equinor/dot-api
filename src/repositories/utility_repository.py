from src.models.utility import Utility
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UtilityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Utility]) -> list[Utility]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Utility]:
        return list(
            (await self.session.scalars(select(Utility).where(Utility.id.in_(ids)))).all()
        )
    
    async def get_all(self) -> list[Utility]:
        return list(
            (await self.session.scalars(select(Utility))).all()
        )
    
    async def update(self, entities: list[Utility]) -> list[Utility]:
        entities_to_update=await self.get([utility.id for utility in entities])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.values=entity.values
            if entity.issue_id:
                entity_to_update=entity.issue_id

        await self.session.flush()
        return entities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
