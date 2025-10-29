import uuid
from typing import List
from pydantic import BaseModel, Field
from src.models.discrete_probability import DiscreteProbability, DiscreteProbabilityParentOption, DiscreteProbabilityParentOutcome
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.outcome_repository import OutcomeRepository

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
    async def to_entity(dto: DiscreteProbabilityIncomingDto, session: AsyncSession ) -> DiscreteProbability:
        if len(dto.parent_option_ids) != 0 or len(dto.parent_outcome_ids) != 0:
            repo = OutcomeRepository(session)        
            outcome_edge_connections, option_edge_connections = await repo.find_edge_connections(
                dto.uncertainty_id, 
                dto.child_outcome_id, 
                dto.parent_option_ids, 
                dto.parent_outcome_ids,
            )
        else: 
            outcome_edge_connections = []
            option_edge_connections = []

        return DiscreteProbability(
            id=dto.id,
            child_outcome_id=dto.child_outcome_id,
            uncertainty_id=dto.uncertainty_id,
            probability=dto.probability,
            parent_outcomes=[DiscreteProbabilityParentOutcome(discrete_probability_id=dto.id, parent_outcome_id=x.connected_node_id, edge_id=x.edge_id) for x in outcome_edge_connections],
            parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=dto.id, parent_option_id=x.connected_node_id, edge_id=x.edge_id) for x in option_edge_connections]
        )

    @staticmethod
    def to_outgoing_dtos(entities: List[DiscreteProbability]) -> List[DiscreteProbabilityOutgoingDto]:
        return [DiscreteProbabilityMapper.to_outgoing_dto(entity) for entity in entities]

    @staticmethod
    async def to_entities(dtos: List[DiscreteProbabilityIncomingDto], session: AsyncSession) -> List[DiscreteProbability]:
        return [await DiscreteProbabilityMapper.to_entity(dto, session) for dto in dtos]