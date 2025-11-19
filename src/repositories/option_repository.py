import uuid
from src.models import Option, Issue, Node, Edge, Decision
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, Session
from sqlalchemy.sql import select
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions
from src.constants import Type


class OptionRepository(BaseRepository[Option, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Option, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[Option]) -> list[Option]:
        entities_to_update = await self.get([option.id for option in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.prepare_entities_for_update([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.decision_id = entity.decision_id
            entity_to_update.name = entity.name
            entity_to_update.utility = entity.utility

        await self.session.flush()
        return entities_to_update

def find_effected_uncertainties(session: Session, entities: set[Option]) -> set[uuid.UUID]:
    uncertainty_ids: set[uuid.UUID] = set()

    parent_decision_ids: list[uuid.UUID] = [x.decision_id for x in entities]

    query = select(Decision).where(Decision.id.in_(parent_decision_ids)).options(
        joinedload(Decision.issue).options(
            joinedload(Issue.node).options(
                selectinload(Node.tail_edges).options(
                    joinedload(Edge.head_node).options(
                        joinedload(Node.issue).options(
                            joinedload(Issue.uncertainty),
                            joinedload(Issue.decision)
                        )
                    )
                )
            )
        )
    )

    decisions: list[Decision] = list((session.scalars(query)).unique().all())

    for decision in decisions:
        for edge in decision.issue.node.tail_edges:
            if edge.head_node.issue.type in [Type.UNCERTAINTY.value, Type.DECISION.value] and edge.head_node.issue.uncertainty:
                uncertainty_ids.add(edge.head_node.issue.uncertainty.id)

    return uncertainty_ids