from src.models import Objective
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ObjectiveRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Objective]) -> list[Objective]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Objective]:
        return list(
            (await self.session.scalars(select(Objective).where(Objective.id.in_(ids)))).all()
        )
    
    async def get_all(self) -> list[Objective]:
        return list(
            (await self.session.scalars(select(Objective))).all()
        )
    
    async def update(self, entities: list[Objective]) -> list[Objective]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.name=entity.name
            enity_to_update.project_id=entity.project_id
            enity_to_update.description=entity.description

        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
