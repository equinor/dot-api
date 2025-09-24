import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.value_metric import ValueMetric
from src.dtos.value_metric_dtos import (
    ValueMetricIncomingDto,
    ValueMetricOutgoingDto,
    ValueMetricMapper,
)
from src.repositories.value_metric_repository import ValueMetricRepository


class ValueMetricService:
    async def create(
        self, session: AsyncSession, dtos: list[ValueMetricIncomingDto]
    ) -> list[ValueMetricOutgoingDto]:
        entities: list[ValueMetric] = await ValueMetricRepository(session).create(
            ValueMetricMapper.to_entities(dtos)
        )
        # get the dtos while the entities are still connected to the session
        result: list[ValueMetricOutgoingDto] = ValueMetricMapper.to_outgoing_dtos(
            entities
        )
        return result

    async def update(
        self, session: AsyncSession, dtos: list[ValueMetricIncomingDto]
    ) -> list[ValueMetricOutgoingDto]:
        entities: list[ValueMetric] = await ValueMetricRepository(session).update(
            ValueMetricMapper.to_entities(dtos)
        )
        # get the dtos while the entities are still connected to the session
        result: list[ValueMetricOutgoingDto] = ValueMetricMapper.to_outgoing_dtos(
            entities
        )
        return result

    async def delete(self, session: AsyncSession, ids: list[uuid.UUID]):
        await ValueMetricRepository(session).delete(ids)

    async def get(
        self, session: AsyncSession, ids: list[uuid.UUID]
    ) -> list[ValueMetricOutgoingDto]:
        entities: list[ValueMetric] = await ValueMetricRepository(session).get(ids)
        result = ValueMetricMapper.to_outgoing_dtos(entities)
        return result

    async def get_all(
        self, session: AsyncSession, odata_query: Optional[str] = None
    ) -> list[ValueMetricOutgoingDto]:
        entities: list[ValueMetric] = await ValueMetricRepository(session).get_all(
            odata_query=odata_query
        )
        result = ValueMetricMapper.to_outgoing_dtos(entities)
        return result
