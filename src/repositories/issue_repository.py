from src.models.issue import Issue
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class IssueRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entities: list[Issue]) -> list[Issue]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def get(self, ids: list[int]) -> list[Issue]:
        query=select(Issue).where(Issue.id.in_(ids)).options(
            *QueryExtensions.load_issue_with_relationships()
        )
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def get_all(self) -> list[Issue]:
        query=select(Issue).options(
            *QueryExtensions.load_issue_with_relationships()

        )
        return list(
            (await self.session.scalars(query)).all()
        )
    
    async def update(self, entities: list[Issue]) -> list[Issue]:
        enities_to_update=await self.get([decision.id for decision in entities])

        for n, enity_to_update in enumerate(enities_to_update):
            entity=entities[n]
            enity_to_update.scenario_id=entity.scenario_id
            enity_to_update.type=entity.type
            enity_to_update.boundary=entity.boundary

            if entity.node:
                enity_to_update.node=await self.session.merge(entity.node)

            if entity.decision:
                enity_to_update.decision=await self.session.merge(entity.decision)

            if entity.uncertainty:
                enity_to_update.uncertainty=await self.session.merge(entity.uncertainty)
            
        await self.session.flush()
        return enities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
