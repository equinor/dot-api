"""DTOs for edge connection operations."""
import uuid
from dataclasses import dataclass
from src.constants import NodeStates
@dataclass
class EdgeConnection:
    """Represents a connection between an outcome and an option/outcome via an edge."""
    
    outcome_id: uuid.UUID
    edge_id: uuid.UUID
    parent_id: uuid.UUID
    parent_type: NodeStates  # "option" or "outcome"
    
    def __init__(
        self,
        outcome_id: uuid.UUID,
        edge_id: uuid.UUID,
        parent_id: uuid.UUID,
        parent_type: NodeStates,
    ):
        self.outcome_id = outcome_id
        self.edge_id = edge_id
        self.parent_id = parent_id
        self.parent_type = parent_type