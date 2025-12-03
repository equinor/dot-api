import uuid
from typing import List
from itertools import product, chain
from src.models.utility import Utility
from src.models import DiscreteUtility, DiscreteUtilityParentOption, DiscreteUtilityParentOutcome
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, Session
from sqlalchemy.sql import select
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions
from src.constants import Type, DecisionHierarchy, Boundary

from src.models import Issue, Node, Edge, Decision, Uncertainty


class UtilityRepository(BaseRepository[Utility, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Utility, query_extension_method=QueryExtensions.empty_load)

    async def update(self, entities: list[Utility]) -> list[Utility]:
        entities_to_update = await self.get([utility.id for utility in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.prepare_entities_for_update([entities, entities_to_update])
        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.values = entity.values
            if entity.issue_id:
                entity_to_update = entity.issue_id

        await self.session.flush()
        return entities_to_update

    async def clear_discrete_utility_tables(self, ids: list[uuid.UUID]):
        
        entities = await self.get(ids)

        for entity in entities:
            entity.discrete_utilities = []

        await self.session.flush()

def recalculate_discrete_utility_table(session: Session, id: uuid.UUID):

    query = (
        select(Utility).where(Utility.id == id).options(
            # TODO: Add selectinload for value metrics when ready
            # selectinload(Utility.value_metrics),
            selectinload(Utility.discrete_utilities).options(
                selectinload(DiscreteUtility.parent_options),
                selectinload(DiscreteUtility.parent_outcomes),
            ),
            joinedload(Utility.issue).options(
                joinedload(Issue.node).options(
                    selectinload(Node.head_edges).options(
                        joinedload(Edge.tail_node).options(
                            joinedload(Node.issue).options(
                                joinedload(Issue.uncertainty).options(
                                    selectinload(Uncertainty.outcomes)
                                ),
                                joinedload(Issue.decision).options(
                                    selectinload(Decision.options)
                                )
                            )
                        )
                    ),
                ),
                joinedload(Issue.utility),
                joinedload(Issue.decision).options(
                    selectinload(Decision.options)
                ),            
            )
        )
    )
    entity: Utility = (session.scalars(query)).unique().first()
    if entity is None:
        return

    entity.discrete_utilities = []

    parent_outcomes_list: List[List[uuid.UUID]] = []
    parent_options_list: List[List[uuid.UUID]] = []

    # filter out duplicate edges (fix later)
    edges = list({(edge.tail_id, edge.head_id): edge for edge in entity.issue.node.head_edges}.values())
    for edge in edges:
        issue = edge.tail_node.issue
        if not issue.boundary in [Boundary.IN.value, Boundary.ON.value]: continue

        if issue.type == Type.UNCERTAINTY:
            # check that this is a key uncertainty
            if not issue.uncertainty or not issue.uncertainty.is_key: continue
            parent_outcomes_list.append([x.id for x in issue.uncertainty.outcomes])

        elif issue.type == Type.DECISION:
            # check that the decision is in focus
            if not issue.decision or issue.decision.type != DecisionHierarchy.FOCUS.value: continue
            parent_options_list.append([x.id for x in issue.decision.options])

    # check if no valid edges and thus cannot be empty, but should be 1 row
    # TODO: Update condition when value metrics are available
    # For now, we just create a single row with no children if there are no parent combinations
    if len(parent_outcomes_list) == 0 and len(parent_options_list) == 0:
        entity.discrete_utilities = [DiscreteUtility(id = uuid.uuid4(), utility_id=entity.id, utility_value=0)]
        session.flush()
        return
    
    parent_combinations = list(product(*parent_outcomes_list, *parent_options_list))
    # get all options and outcomes to filter on later
    all_options: List[uuid.UUID] = list(chain(*parent_options_list))
    all_outcomes: List[uuid.UUID] = list(chain(*parent_outcomes_list))

    # TODO: Loop through value metrics instead when available
    # For now, create one row per parent combination
    for parent_combination in parent_combinations:
        parent_option_ids = filter(lambda x: x in all_options, parent_combination)
        parent_outcome_ids = filter(lambda x: x in all_outcomes, parent_combination)
        utility_id = uuid.uuid4() 
        entity.discrete_utilities.append(
            DiscreteUtility(
                id = utility_id,
                utility_id=entity.id,
                # child_value_metric_id=...,  # TODO: Add when ready
                utility_value=0,
                parent_outcomes=[DiscreteUtilityParentOutcome(discrete_utility_id=utility_id, parent_outcome_id=x) for x in parent_outcome_ids],
                parent_options=[DiscreteUtilityParentOption(discrete_utility_id=utility_id, parent_option_id=x) for x in parent_option_ids],
            )
        )

    session.flush([entity])
    return
