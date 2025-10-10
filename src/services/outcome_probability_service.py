import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.outcome_probability import OutcomeProbability
from src.dtos.outcome_probability_dtos import (
    OutcomeProbabilityIncomingDto,
    OutcomeProbabilityOutgoingDto,
    OutcomeProbabilityMapper,
)
from src.repositories.outcome_probability_repository import OutcomeProbabilityRepository


class OutcomeProbabilityService:
    async def create(
        self, session: AsyncSession, dtos: list[OutcomeProbabilityIncomingDto]
    ) -> list[OutcomeProbabilityOutgoingDto]:
        entities: list[OutcomeProbability] = await OutcomeProbabilityRepository(session).create(
            OutcomeProbabilityMapper.to_entities(dtos)
        )
        # get the dtos while the entities are still connected to the session
        result: list[OutcomeProbabilityOutgoingDto] = OutcomeProbabilityMapper.to_outgoing_dtos(entities)
        return result

    async def update(
        self, session: AsyncSession, dtos: list[OutcomeProbabilityIncomingDto]
    ) -> list[OutcomeProbabilityOutgoingDto]:
        entities: list[OutcomeProbability] = await OutcomeProbabilityRepository(session).update(
            OutcomeProbabilityMapper.to_entities(dtos)
        )
        # get the dtos while the entities are still connected to the session
        result: list[OutcomeProbabilityOutgoingDto] = OutcomeProbabilityMapper.to_outgoing_dtos(entities)
        return result

    async def delete(self, session: AsyncSession, ids: list[uuid.UUID]):
        await OutcomeProbabilityRepository(session).delete(ids)

    async def get(
        self, session: AsyncSession, ids: list[uuid.UUID]
    ) -> list[OutcomeProbabilityOutgoingDto]:
        outcome_probabilities: list[OutcomeProbability] = await OutcomeProbabilityRepository(session).get(ids)
        result = OutcomeProbabilityMapper.to_outgoing_dtos(outcome_probabilities)
        return result

    async def get_all(
        self, session: AsyncSession, odata_query: Optional[str] = None
    ) -> list[OutcomeProbabilityOutgoingDto]:
        outcome_probabilities: list[OutcomeProbability] = await OutcomeProbabilityRepository(session).get_all(
            odata_query=odata_query
        )
        result = OutcomeProbabilityMapper.to_outgoing_dtos(outcome_probabilities)
        return result