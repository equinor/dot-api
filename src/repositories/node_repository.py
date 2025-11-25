import uuid
from typing import List, Dict, Any
from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from src.repositories.query_extensions import QueryExtensions
from src.repositories.base_repository import BaseRepository
from src.constants import NodeStates
from src.dtos.edge_connection_dtos import EdgeConnection
from src.models import (
    Node, 
    Issue, 
    Uncertainty, 
    Edge, 
    Decision
)
from src.constants import DecisionHierarchy, Boundary, Type

@dataclass
class UncertaintyConnectionRequest:
    """Data structure for requesting edge connections for a specific uncertainty and outcome."""
    outcome_id: uuid.UUID
    option_ids: List[uuid.UUID]
    outcome_ids: List[uuid.UUID]


class NodeRepository(BaseRepository[Node, uuid.UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session,
            Node,
            query_extension_method=QueryExtensions.load_node_with_relationships,
        )

    async def update(self, entities: list[Node]) -> list[Node]:
        entities_to_update = await self.get([node.id for node in entities])
        # sort the entity lists to share the same order according to the entity.id
        self.prepare_entities_for_update([entities, entities_to_update])

        for n, entity_to_update in enumerate(entities_to_update):
            entity = entities[n]
            entity_to_update.scenario_id = entity.scenario_id
            if entity.issue_id:
                entity_to_update.issue_id = entity.issue_id
            if entity.node_style:
                entity_to_update.node_style = await self.session.merge(entity.node_style)

        await self.session.flush()
        return entities_to_update
    
    async def clear_discrete_probability_tables(self, ids: list[uuid.UUID]):
        
        entities = await self.get(ids)

        for entity in entities:
            if entity.issue.uncertainty is None: continue
            entity.issue.uncertainty.discrete_probabilities = []

        await self.session.flush()
