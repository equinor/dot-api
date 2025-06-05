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
        entities_to_update=await self.get([decision.id for decision in entities])

        for n, entity_to_update in enumerate(entities_to_update):
            entity=entities[n]
            entity_to_update.scenario_id=entity.scenario_id
            entity_to_update.type=entity.type
            entity_to_update.boundary=entity.boundary

            if entity.node:
                entity_to_update.node=await self.session.merge(entity.node)

            if entity.decision:
                entity_to_update.decision=await self.session.merge(entity.decision)

            if entity.uncertainty:
                entity_to_update.uncertainty=await self.session.merge(entity.uncertainty)

            if entity.utility:
                entity_to_update.utility=await self.session.merge(entity.utility)
                
            if entity.value_metric:
                entity_to_update.value_metric=await self.session.merge(entity.value_metric)
            
        await self.session.flush()
        return entities_to_update
    
    async def delete(self, ids: list[int]) -> None:
        entities=await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()
