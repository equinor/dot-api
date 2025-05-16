from src.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.repositories.query_extensions import (
    load_project_relations_all,
    load_project_relations_basic,
)

class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Project]) -> list[Project]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Project]:
        query=select(Project).where(Project.id.in_(ids)).options(
            *load_project_relations_basic()
        )
        return list(
            (await self.session.scalars(query)).all()
        )
    async def get_all(self) -> list[Project]:
    
        query=select(Project).options(
            *load_project_relations_basic()
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
            enity_to_update.objectives=entity.objectives
            enity_to_update.opportunities=entity.opportunities
        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()

    async def get_project_full_projection(self) -> list[Project]:
        query=select(Project).options(
            *load_project_relations_all()
        )
        return list(
            (await self.session.scalars(query)).all()
        )