"""DTOs for edge connection operations."""
import uuid
from dataclasses import dataclass
from src.constants import NodeStates
@dataclass
class EdgeConnection:
    """Represents a connection between an outcome and an option/outcome via an edge."""
    
    outcome_id: uuid.UUID
    edge_id: uuid.UUID
    connected_node_id: uuid.UUID
    connected_node_type: NodeStates  # "option" or "outcome"
    
    def __init__(
        self,
        outcome_id: uuid.UUID,
        edge_id: uuid.UUID,
        connected_node_id: uuid.UUID,
        connected_node_type: NodeStates,
    ):
        self.outcome_id = outcome_id
        self.edge_id = edge_id
        self.connected_node_id = connected_node_id
        self.connected_node_type = connected_node_type