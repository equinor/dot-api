from typing import Optional
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions

class UserRepository(BaseRepository[User, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User, query_extension_method=QueryExtensions.empty_load)

    async def get_or_create(self, entity: User) -> User:
        user=await self.get_by_azure_id(entity.azure_id)
        if user is None:
            user = await self.create_single(entity)
        return user
    
    async def get_by_azure_id(self, azure_id: str) -> Optional[User]:
        return (await self.session.scalars(select(User).where(User.azure_id==azure_id))).first()
    
    async def update(self, entities: list[User]) -> list[User]:
        entities_to_update=await self.get([decision.id for decision in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.name=entity.name
            entity_to_update.azure_id=entity.azure_id

        await self.session.flush()
        return entities_to_update

        
