from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models import Probability
from src.dtos.probability_dtos import (
    ProbabilityIncomingDto, 
    ProbabilityOutgoingDto, 
    ProbabilityMapper
)
from src.repositories.probability_repository import ProbabilityRepository

class ProbabilityService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[ProbabilityIncomingDto]) -> list[ProbabilityOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                entities: list[Probability] = await ProbabilityRepository(session).create(ProbabilityMapper.to_entities(dtos))
                # get the dtos while the entities are still connected to the session
                result: list[ProbabilityOutgoingDto] = ProbabilityMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def update(self, dtos: list[ProbabilityIncomingDto]) -> list[ProbabilityOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                entities: list[Probability] = await ProbabilityRepository(session).update(ProbabilityMapper.to_entities(dtos))
                # get the dtos while the entities are still connected to the session
                result: list[ProbabilityOutgoingDto] = ProbabilityMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def delete(self, ids: list[int]):
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                await ProbabilityRepository(session).delete(ids)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get(self, ids: list[int]) -> list[ProbabilityOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            decisions: list[Probability] = await ProbabilityRepository(session).get(ids)
            result=ProbabilityMapper.to_outgoing_dtos(decisions)
        return result
    
    async def get_all(self) -> list[ProbabilityOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            decisions: list[Probability] = await ProbabilityRepository(session).get_all()
            result=ProbabilityMapper.to_outgoing_dtos(decisions)
        return result