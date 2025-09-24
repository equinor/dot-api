import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.opportunity import Opportunity
from src.dtos.opportunity_dtos import (
    OpportunityIncomingDto,
    OpportunityOutgoingDto,
    OpportunityMapper,
)
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserMapper,
)
from src.repositories.opportunity_repository import OpportunityRepository
from src.repositories.user_repository import UserRepository


class OpportunityService:
    async def create(
        self,
        session: AsyncSession,
        dtos: list[OpportunityIncomingDto],
        user_dto: UserIncomingDto,
    ) -> list[OpportunityOutgoingDto]:
        user = await UserRepository(session).get_or_create(
            UserMapper.to_entity(user_dto)
        )
        entities: list[Opportunity] = await OpportunityRepository(session).create(
            OpportunityMapper.to_entities(dtos, user.id)
        )
        # get the dtos while the entities are still connected to the session
        result: list[OpportunityOutgoingDto] = OpportunityMapper.to_outgoing_dtos(
            entities
        )
        return result

    async def update(
        self,
        session: AsyncSession,
        dtos: list[OpportunityIncomingDto],
        user_dto: UserIncomingDto,
    ) -> list[OpportunityOutgoingDto]:
        user = await UserRepository(session).get_or_create(
            UserMapper.to_entity(user_dto)
        )
        entities: list[Opportunity] = await OpportunityRepository(session).update(
            OpportunityMapper.to_entities(dtos, user.id)
        )
        # get the dtos while the entities are still connected to the session
        result: list[OpportunityOutgoingDto] = OpportunityMapper.to_outgoing_dtos(
            entities
        )
        return result

    async def delete(self, session: AsyncSession, ids: list[uuid.UUID]):
        await OpportunityRepository(session).delete(ids)

    async def get(
        self, session: AsyncSession, ids: list[uuid.UUID]
    ) -> list[OpportunityOutgoingDto]:
        opportunities: list[Opportunity] = await OpportunityRepository(session).get(ids)
        result = OpportunityMapper.to_outgoing_dtos(opportunities)
        return result

    async def get_all(
        self, session: AsyncSession, odata_query: Optional[str] = None
    ) -> list[OpportunityOutgoingDto]:
        opportunities: list[Opportunity] = await OpportunityRepository(session).get_all(
            odata_query=odata_query
        )
        result = OpportunityMapper.to_outgoing_dtos(opportunities)
        return result
