import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.option import Option
from src.dtos.option_dtos import OptionIncomingDto, OptionOutgoingDto, OptionMapper
from src.repositories.option_repository import OptionRepository


class OptionService:
    async def create(
        self, session: AsyncSession, dtos: list[OptionIncomingDto]
    ) -> list[OptionOutgoingDto]:
        entities: list[Option] = await OptionRepository(session).create(
            OptionMapper.to_entities(dtos)
        )
        # get the dtos while the entities are still connected to the session
        result: list[OptionOutgoingDto] = OptionMapper.to_outgoing_dtos(entities)
        return result

    async def update(
        self, session: AsyncSession, dtos: list[OptionIncomingDto]
    ) -> list[OptionOutgoingDto]:
        entities: list[Option] = await OptionRepository(session).update(
            OptionMapper.to_entities(dtos)
        )
        # get the dtos while the entities are still connected to the session
        result: list[OptionOutgoingDto] = OptionMapper.to_outgoing_dtos(entities)
        return result

    async def delete(self, session: AsyncSession, ids: list[uuid.UUID]):
        await OptionRepository(session).delete(ids)

    async def get(
        self, session: AsyncSession, ids: list[uuid.UUID]
    ) -> list[OptionOutgoingDto]:
        options: list[Option] = await OptionRepository(session).get(ids)
        result = OptionMapper.to_outgoing_dtos(options)
        return result

    async def get_all(
        self, session: AsyncSession, odata_query: Optional[str] = None
    ) -> list[OptionOutgoingDto]:
        options: list[Option] = await OptionRepository(session).get_all(
            odata_query=odata_query
        )
        result = OptionMapper.to_outgoing_dtos(options)
        return result
