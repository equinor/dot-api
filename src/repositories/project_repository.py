from src.models.project import Project
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Project]) -> list[Project]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Project]:
        query=select(Project).where(Project.id.in_(ids)).options(
            *QueryExtensions.load_project_with_relationships()
        )
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def get_all(self) -> list[Project]:
        query=select(Project).options(
            *QueryExtensions.load_project_with_relationships()
        )
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def update(self, entities: list[Project]) -> list[Project]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.name=entity.name
            enity_to_update.description=entity.description
            
        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
