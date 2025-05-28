from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.uncertainty import Uncertainty
from src.dtos.uncertainty_dtos import (
    UncertaintyIncomingDto, 
    UncertaintyOutgoingDto, 
    UncertaintyMapper
)
from src.repositories.uncertainty_repository import UncertaintyRepository

class UncertaintyService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[UncertaintyIncomingDto]) -> list[UncertaintyOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                entities: list[Uncertainty] = await UncertaintyRepository(session).create(UncertaintyMapper.to_entities(dtos))
                # get the dtos while the entities are still connected to the session
                result: list[UncertaintyOutgoingDto] = UncertaintyMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def update(self, dtos: list[UncertaintyIncomingDto]) -> list[UncertaintyOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                entities: list[Uncertainty] = await UncertaintyRepository(session).update(UncertaintyMapper.to_entities(dtos))
                # get the dtos while the entities are still connected to the session
                result: list[UncertaintyOutgoingDto] = UncertaintyMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def delete(self, ids: list[int]):
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                await UncertaintyRepository(session).delete(ids)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get(self, ids: list[int]) -> list[UncertaintyOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            decisions: list[Uncertainty] = await UncertaintyRepository(session).get(ids)
            result=UncertaintyMapper.to_outgoing_dtos(decisions)
        return result
    
    async def get_all(self) -> list[UncertaintyOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            decisions: list[Uncertainty] = await UncertaintyRepository(session).get_all()
            result=UncertaintyMapper.to_outgoing_dtos(decisions)
        return result