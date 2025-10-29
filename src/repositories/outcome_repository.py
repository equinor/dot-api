import uuid
from typing import List
from src.constants import NodeStates
from sqlalchemy import select
from src.models.outcome import Outcome
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.repositories.query_extensions import QueryExtensions
from src.dtos.edge_connection_dtos import EdgeConnection
from src.models.node import Node
from src.models.issue import Issue
from src.models.uncertainty import Uncertainty

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
    
    async def find_edge_connections(
        self, 
        uncertainty_id: uuid.UUID,
        outcome_id: uuid.UUID, 
        option_ids: List[uuid.UUID], 
        outcome_ids: List[uuid.UUID]
    ) -> tuple[List[EdgeConnection], List[EdgeConnection]]:
        """
        Find all edges that connect to the node containing the child outcome and create
        DiscreteProbabilityParentOption/Outcome relationships for the provided options/outcomes.
        
        Args:
            outcome_id: The ID of the child outcome to find connections for
            option_ids: List of option IDs to create connections for
            outcome_ids: List of other outcome IDs to create connections for
            
        Returns:
            List of EdgeConnection objects representing the connections created
        """
        
        
        outcome_connections: List[EdgeConnection] = []
        option_connections: List[EdgeConnection] = []
        
        # First, get the outcome to find its uncertainty and related node
        outcome_query = select(Outcome).where(Outcome.id == outcome_id)
        outcome_result = await self.session.scalar(outcome_query)
        
        if outcome_result is None or outcome_result.uncertainty_id != uncertainty_id:
            raise ValueError("Outcome not found or does not belong to the specified uncertainty")
            
        # Find the node that contains this outcome's uncertainty
        uncertainty_node_query = (
            select(Node)
            .where(Node.issue.has(Issue.uncertainty.has(Uncertainty.id == uncertainty_id)))
            .options(
                *QueryExtensions.load_node_with_edge_relationships()
            )
        )
        
        uncertainty_node = await self.session.scalar(uncertainty_node_query)
        
        if not uncertainty_node:
            raise ValueError("Uncertainty node not found")
            
        # Process option connections
        if option_ids:
            for edge in uncertainty_node.head_edges:
                if edge.tail_node.issue.decision is None or len(edge.tail_node.issue.decision.options) == 0: 
                    continue
                edge_options = edge.tail_node.issue.decision.options
                for option in edge_options:
                    if option.id in option_ids:
                        option_connections.append(EdgeConnection(
                            outcome_id=outcome_id,
                            edge_id=edge.id,
                            connected_node_id=option.id,
                            connected_node_type=NodeStates.OPTION
                        ))
        
        # Process outcome connections
        if outcome_ids:
            for edge in uncertainty_node.head_edges:
                if edge.tail_node.issue.uncertainty is None or len(edge.tail_node.issue.uncertainty.outcomes) == 0: 
                    continue
                edge_outcomes = edge.tail_node.issue.uncertainty.outcomes
                for outcome in edge_outcomes:
                    if outcome.id in outcome_ids:
                        outcome_connections.append(EdgeConnection(
                            outcome_id=outcome_id,
                            edge_id=edge.id,
                            connected_node_id=outcome.id,
                            connected_node_type=NodeStates.OUTCOME
                        ))
        
        return outcome_connections, option_connections
    