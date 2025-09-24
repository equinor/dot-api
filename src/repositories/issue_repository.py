import uuid
from src.models.issue import Issue
from src.repositories.query_extensions import QueryExtensions
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository


class IssueRepository(BaseRepository[Issue, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session,
            Issue,
            query_extension_method=QueryExtensions.load_issue_with_relationships,
        )

    async def update(self, entities: list[Issue]) -> list[Issue]:
        entities_to_update = await self.get([decision.id for decision in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.sort_entity_collections_by_id([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.scenario_id = entity.scenario_id
            entity_to_update.type = entity.type
            entity_to_update.boundary = entity.boundary
            entity_to_update.name = entity.name
            entity_to_update.description = entity.description
            entity_to_update.order = entity.order

            if entity.node:
                entity_to_update.node = await self.session.merge(entity.node)

            if entity.decision:
                entity_to_update.decision = await self.session.merge(entity.decision)

            if entity.uncertainty:
                entity_to_update.uncertainty = await self.session.merge(entity.uncertainty)

            if entity.utility:
                entity_to_update.utility = await self.session.merge(entity.utility)

            if entity.value_metric:
                entity_to_update.value_metric = await self.session.merge(entity.value_metric)

        await self.session.flush()
        return entities_to_update
