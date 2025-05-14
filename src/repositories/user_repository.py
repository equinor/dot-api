from typing import Optional
from src.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, entity: User) -> User:
        user=await self.get_by_azure_id(entity.azure_id)
        if user is None:
            user = await self.create(entity)
        return user

    async def create(self, entity: User) -> User:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def create_all(self, entities: list[User]) -> list[User]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[User]:
        return list(
            (await self.session.scalars(select(User).where(User.id.in_(ids)))).all()
        )
    
    async def get_all(self) -> list[User]:
        return list(
            (await self.session.scalars(select(User))).all()
        )
    
    async def get_by_azure_id(self, azure_id: str) -> Optional[User]:
        return (await self.session.scalars(select(User).where(User.azure_id==azure_id))).first()
    
    async def update(self, entities: list[User]) -> list[User]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.name=entity.name
            enity_to_update.azure_id=entity.azure_id

        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
