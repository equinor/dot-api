from typing import Optional
import uuid
from src.dtos.project_contributors_dtos import ProjectContributorMapper
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.orm import selectinload
from src.dtos.project_dtos import AccessibleProjectsDto

class UserRepository(BaseRepository[User, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User, query_extension_method=QueryExtensions.load_user_with_roles)

    async def get_or_create(self, entity: User) -> User:
        user=await self.get_by_azure_id(entity.azure_id)
        if user is None:
            user = await self.create_single(entity)
        return user
    
    async def get_by_azure_id(self, azure_id: str) -> Optional[User]:
        return (await self.session.scalars(select(User).where(User.azure_id==azure_id))).first()
    
    async def update(self, entities: list[User]) -> list[User]:
        entities_to_update=await self.get([decision.id for decision in entities])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.name=entity.name
            entity_to_update.azure_id=entity.azure_id

        await self.session.flush()
        return entities_to_update
    # from sqlalchemy.orm import selectinload  # Already imported at the top

    async def get_accessible_projects_by_user(self, id: int) -> dict[str, list[uuid.UUID]]:
        user_with_roles = self.query_extension_method().where(User.id == id)
        user = (await self.session.scalars(user_with_roles)).first()
        if user is None:
            return {"contributor": [], "owner": []}
        contributor_projects_ids: list[uuid.UUID] = [project.project_id for project in user.project_contributors]
        owner_projects_ids: list[uuid.UUID] = [project.project_id for project in user.project_owners]
        return AccessibleProjectsDto(
            contributor_projects_ids=contributor_projects_ids,
            owner_projects_ids=owner_projects_ids
        )
