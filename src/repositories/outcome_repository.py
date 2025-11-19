import uuid
from src.models import (
    Outcome, 
    Uncertainty, 
    Issue, 
    Edge, 
    Node,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql import select
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions
from src.constants import Type

class OutcomeRepository(BaseRepository[Outcome, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Outcome, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[Outcome]) -> list[Outcome]:
        entities_to_update = await self.get([outcome.id for outcome in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.prepare_entities_for_update([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.uncertainty_id = entity.uncertainty_id
            entity_to_update.name = entity.name
            entity_to_update.utility = entity.utility
            

        await self.session.flush()
        return entities_to_update
    

def find_effected_uncertainties(session: Session, entities: set[Outcome]) -> set[uuid.UUID]:
    uncertainty_ids: set[uuid.UUID] = set()

    parent_uncertainty_ids: list[uuid.UUID] = [x.uncertainty_id for x in entities]

    query = select(Uncertainty).where(Uncertainty.id.in_(parent_uncertainty_ids)).options(
        joinedload(Uncertainty.issue).options(
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

    uncertainties: list[Uncertainty] = list((session.scalars(query)).unique().all())

    for uncertainty in uncertainties:
        uncertainty_ids.add(uncertainty.id)
        for edge in uncertainty.issue.node.tail_edges:
            if edge.head_node.issue.type in [Type.UNCERTAINTY.value, Type.DECISION.value] and edge.head_node.issue.uncertainty:
                uncertainty_ids.add(edge.head_node.issue.uncertainty.id)

    return uncertainty_ids