from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models import Decision
from dtos.decision_dtos import (
    DecisionIncommingDto, 
    DecisionOutgoingDto, 
    DecisionMapper
)
from repositories.decision_repository import DecisionRepository

class DecisionService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[DecisionIncommingDto]) -> list[DecisionOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                decisions: list[Decision] = await DecisionRepository(session).create(DecisionMapper.to_entities(dtos))
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return DecisionMapper.to_outgoing_dtos(decisions)
    
    async def get(self, ids: list[int]) -> list[DecisionOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            decisions: list[Decision] = await DecisionRepository(session).retrieve(ids)
        return DecisionMapper.to_outgoing_dtos(decisions)