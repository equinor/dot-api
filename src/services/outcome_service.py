import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.outcome import Outcome
from src.dtos.outcome_dtos import (
    OutcomeIncomingDto,
    OutcomeOutgoingDto,
    OutcomeMapper,
)
from src.repositories.outcome_repository import OutcomeRepository


class OutcomeService:
    async def create(
        self, session: AsyncSession, dtos: list[OutcomeIncomingDto]
    ) -> list[OutcomeOutgoingDto]:
        entities: list[Outcome] = await OutcomeRepository(session).create(
            OutcomeMapper.to_entities(dtos)
        )
        # get the dtos while the entities are still connected to the session
        result: list[OutcomeOutgoingDto] = OutcomeMapper.to_outgoing_dtos(entities)
        return result

    async def update(
        self, session: AsyncSession, dtos: list[OutcomeIncomingDto]
    ) -> list[OutcomeOutgoingDto]:
        entities: list[Outcome] = await OutcomeRepository(session).update(
            OutcomeMapper.to_entities(dtos)
        )
        # get the dtos while the entities are still connected to the session
        result: list[OutcomeOutgoingDto] = OutcomeMapper.to_outgoing_dtos(entities)
        return result

    async def delete(self, session: AsyncSession, ids: list[uuid.UUID]):
        await OutcomeRepository(session).delete(ids)

    async def get(self, session: AsyncSession, ids: list[uuid.UUID]) -> list[OutcomeOutgoingDto]:
        outcomes: list[Outcome] = await OutcomeRepository(session).get(ids)
        result = OutcomeMapper.to_outgoing_dtos(outcomes)
        return result

    async def get_all(
        self, session: AsyncSession, odata_query: Optional[str] = None
    ) -> list[OutcomeOutgoingDto]:
        outcomes: list[Outcome] = await OutcomeRepository(session).get_all(odata_query=odata_query)
        result = OutcomeMapper.to_outgoing_dtos(outcomes)
        return result
