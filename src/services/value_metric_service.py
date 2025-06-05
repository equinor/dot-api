from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.value_metric import ValueMetric
from src.dtos.value_metric_dtos import (
    ValueMetricIncomingDto, 
    ValueMetricOutgoingDto, 
    ValueMetricMapper
)
from src.repositories.value_metric_repository import ValueMetricRepository
from src.services.session_handler import session_handler

class ValueMetricService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[ValueMetricIncomingDto]) -> list[ValueMetricOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[ValueMetric] = await ValueMetricRepository(session).create(ValueMetricMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[ValueMetricOutgoingDto] = ValueMetricMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[ValueMetricIncomingDto]) -> list[ValueMetricOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[ValueMetric] = await ValueMetricRepository(session).update(ValueMetricMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[ValueMetricOutgoingDto] = ValueMetricMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[int]):
        async with session_handler(self.engine) as session:
            await ValueMetricRepository(session).delete(ids)
    
    async def get(self, ids: list[int]) -> list[ValueMetricOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[ValueMetric] = await ValueMetricRepository(session).get(ids)
            result=ValueMetricMapper.to_outgoing_dtos(entities)
        return result
    
    async def get_all(self) -> list[ValueMetricOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[ValueMetric] = await ValueMetricRepository(session).get_all()
            result=ValueMetricMapper.to_outgoing_dtos(entities)
        return result