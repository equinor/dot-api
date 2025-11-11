import uuid
from typing import List, Dict
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

    async def find_edge_connections_to_node(
            self,
            uncertainty_node: Node,
            outcome_id: uuid.UUID, 
            option_ids: List[uuid.UUID], 
            outcome_ids: List[uuid.UUID]
    ) -> tuple[List[EdgeConnection], List[EdgeConnection]]:
        
        
        if not uncertainty_node:
            raise ValueError("Uncertainty node not found")
        
        option_ids_set: set[uuid.UUID] = set(option_ids) if option_ids else set()
        outcome_ids_set: set[uuid.UUID] = set(outcome_ids) if outcome_ids else set()
        
        outcome_connections: List[EdgeConnection] = []
        option_connections: List[EdgeConnection] = []
        
        for edge in uncertainty_node.head_edges:
            tail_issue = edge.tail_node.issue
            if not tail_issue.boundary in [Boundary.IN.value, Boundary.ON.value]: continue

            # Process option connections if this edge leads to a decision node
            if option_ids_set and tail_issue.decision and tail_issue.decision.options and tail_issue.type == Type.DECISION.value and tail_issue.decision.type==DecisionHierarchy.FOCUS.value:
                for option in tail_issue.decision.options:
                    if option.id in option_ids_set:
                        option_connections.append(EdgeConnection(
                            outcome_id=outcome_id,
                            edge_id=edge.id,
                            parent_id=option.id,
                            parent_type=NodeStates.OPTION
                        ))
            
            # Process outcome connections if this edge leads to an uncertainty node
            if outcome_ids_set and tail_issue.uncertainty and tail_issue.uncertainty.outcomes and tail_issue.type == Type.UNCERTAINTY.value and tail_issue.uncertainty.is_key:
                for outcome in tail_issue.uncertainty.outcomes:
                    if outcome.id in outcome_ids_set:
                        outcome_connections.append(EdgeConnection(
                            outcome_id=outcome_id,
                            edge_id=edge.id,
                            parent_id=outcome.id,
                            parent_type=NodeStates.OUTCOME
                        ))
        return outcome_connections, option_connections
    
    async def find_edge_connections_for_multiple_uncertainties(
        self,
        uncertainty_requests: Dict[uuid.UUID, UncertaintyConnectionRequest]
    ) -> Dict[uuid.UUID, tuple[List[EdgeConnection], List[EdgeConnection]]]:
        """
        Find all edges that connect to multiple uncertainty nodes and create
        DiscreteProbabilityParentOption/Outcome relationships for the provided options/outcomes.
        Performs a single query to fetch all uncertainty nodes and then reuses find_edge_connections_from_node
        for each uncertainty.
        
        Args:
            uncertainty_requests: Dictionary mapping uncertainty_id to UncertaintyConnectionRequest containing:
                - outcome_id: The ID of the child outcome to find connections for
                - option_ids: List of option IDs to create connections for
                - outcome_ids: List of other outcome IDs to create connections for
            
        Returns:
            Dictionary mapping uncertainty_id to tuple of (outcome_connections, option_connections) EdgeConnection lists
        """
        if not uncertainty_requests:
            return {}
        
        uncertainty_ids = list(uncertainty_requests.keys())
        
        # Single query to fetch all uncertainty nodes
        uncertainty_nodes_query = (
            select(Node)
            .where(Node.issue.has(Issue.uncertainty.has(Uncertainty.id.in_(uncertainty_ids))))
            .options(
                joinedload(Node.issue).options(
                    joinedload(Issue.uncertainty)
                ),
                selectinload(Node.head_edges).options(
                    joinedload(Edge.tail_node).options(
                        joinedload(Node.issue).options(
                            joinedload(Issue.decision).options(
                                selectinload(Decision.options)
                            ),
                            joinedload(Issue.uncertainty).options(
                                selectinload(Uncertainty.outcomes)
                            ),
                        ),
                    )
                )
            )
        )
        
        uncertainty_nodes = (await self.session.scalars(uncertainty_nodes_query)).all()
        
        # Create a mapping of uncertainty_id to node for quick lookup
        uncertainty_node_map: Dict[uuid.UUID, Node] = {}
        for node in uncertainty_nodes:
            if node.issue and node.issue.uncertainty:
                uncertainty_node_map[node.issue.uncertainty.id] = node
        
        # Process each uncertainty using the existing find_edge_connections_from_node method
        results: Dict[uuid.UUID, tuple[List[EdgeConnection], List[EdgeConnection]]] = {}
        
        for uncertainty_id, request in uncertainty_requests.items():
            uncertainty_node = uncertainty_node_map.get(uncertainty_id)
            if uncertainty_node:
                connections = await self.find_edge_connections_to_node(
                    uncertainty_node,
                    request.outcome_id,
                    request.option_ids,
                    request.outcome_ids
                )
                results[uncertainty_id] = connections
            else:
                # If uncertainty node not found, return empty lists
                results[uncertainty_id] = ([], [])
        
        return results
    
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
        
        This method now uses the optimized find_edge_connections_for_multiple_uncertainties method
        for consistency and potential future performance benefits.
        
        Args:
            uncertainty_id: The ID of the uncertainty node
            outcome_id: The ID of the child outcome to find connections for
            option_ids: List of option IDs to create connections for
            outcome_ids: List of other outcome IDs to create connections for
            
        Returns:
            Tuple of (outcome_connections, option_connections) EdgeConnection lists
        """
        # Use the multiple uncertainties method with a single uncertainty for consistency
        request = UncertaintyConnectionRequest(
            outcome_id=outcome_id,
            option_ids=option_ids,
            outcome_ids=outcome_ids
        )
        
        results = await self.find_edge_connections_for_multiple_uncertainties({
            uncertainty_id: request
        })
        
        # Return the result for the single uncertainty, or empty lists if not found
        return results.get(uncertainty_id, ([], []))           
    