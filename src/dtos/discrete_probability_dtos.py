import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.discrete_probability import DiscreteProbability, DiscreteProbabilityParentOption, DiscreteProbabilityParentOutcome
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.node_repository import NodeRepository, UncertaintyConnectionRequest
from src.dtos.edge_connection_dtos import EdgeConnection

class DiscreteProbabilityDto(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    uncertainty_id: uuid.UUID
    child_outcome_id: uuid.UUID
    probability: float = 0.0
    parent_outcome_ids: List[uuid.UUID] = []
    parent_option_ids: List[uuid.UUID] = []

class DiscreteProbabilityIncomingDto(DiscreteProbabilityDto):
    pass

class DiscreteProbabilityOutgoingDto(DiscreteProbabilityDto):
    pass

class DiscreteProbabilityMapper:
    @staticmethod
    def to_outgoing_dto(entity: DiscreteProbability) -> DiscreteProbabilityOutgoingDto:
        return DiscreteProbabilityOutgoingDto(
            id=entity.id,
            child_outcome_id=entity.child_outcome_id,
            uncertainty_id=entity.uncertainty_id,
            probability=entity.probability,
            parent_outcome_ids=[x.parent_outcome_id for x in entity.parent_outcomes] if entity.parent_outcomes else [],
            parent_option_ids=[x.parent_option_id for x in entity.parent_options] if entity.parent_options else [],
        )

    @staticmethod
    async def to_entity(dto: DiscreteProbabilityIncomingDto, session: AsyncSession, edge_connection_result: Optional[tuple[List[EdgeConnection], List[EdgeConnection]]] = None) -> DiscreteProbability:
        if edge_connection_result is None:
            repo = NodeRepository(session)        
            outcome_edge_connections, option_edge_connections = await repo.find_edge_connections(
                dto.uncertainty_id, 
                dto.child_outcome_id, 
                dto.parent_option_ids, 
                dto.parent_outcome_ids,
            )
        else: 
            outcome_edge_connections, option_edge_connections = edge_connection_result

        return DiscreteProbability(
            id=dto.id,
            child_outcome_id=dto.child_outcome_id,
            uncertainty_id=dto.uncertainty_id,
            probability=dto.probability,
            parent_outcomes=[DiscreteProbabilityParentOutcome(discrete_probability_id=dto.id, parent_outcome_id=x.parent_id, edge_id=x.edge_id) for x in outcome_edge_connections],
            parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=dto.id, parent_option_id=x.parent_id, edge_id=x.edge_id) for x in option_edge_connections]
        )

    @staticmethod
    def to_outgoing_dtos(entities: List[DiscreteProbability]) -> List[DiscreteProbabilityOutgoingDto]:
        return [DiscreteProbabilityMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    async def to_entities(dtos: List[DiscreteProbabilityIncomingDto], session: AsyncSession) -> List[DiscreteProbability]:
        repo = NodeRepository(session)
        edge_connections = await repo.find_edge_connections_for_multiple_uncertainties(
            {dto.uncertainty_id: UncertaintyConnectionRequest(
                outcome_id=dto.child_outcome_id,
                option_ids=dto.parent_option_ids,
                outcome_ids=dto.parent_outcome_ids
            ) for dto in dtos}
        )
        return [await DiscreteProbabilityMapper.to_entity(dto, session, edge_connections[dto.uncertainty_id]) for dto in dtos]