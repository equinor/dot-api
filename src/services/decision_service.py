from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models import Decision
from src.dtos.decision_dtos import (
    DecisionIncomingDto, 
    DecisionOutgoingDto, 
    DecisionMapper
)
from src.repositories.decision_repository import DecisionRepository

class DecisionService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[DecisionIncomingDto]) -> list[DecisionOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                entities: list[Decision] = await DecisionRepository(session).create(DecisionMapper.to_entities(dtos))
                # get the dtos while the entities are still connected to the session
                result: list[DecisionOutgoingDto] = DecisionMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def update(self, dtos: list[DecisionIncomingDto]) -> list[DecisionOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                entities: list[Decision] = await DecisionRepository(session).update(DecisionMapper.to_entities(dtos))
                # get the dtos while the entities are still connected to the session
                result: list[DecisionOutgoingDto] = DecisionMapper.to_outgoing_dtos(entities)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
        return result
    
    async def delete(self, ids: list[int]):
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            try:
                await DecisionRepository(session).delete(ids)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def get(self, ids: list[int]) -> list[DecisionOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            decisions: list[Decision] = await DecisionRepository(session).get(ids)
            result=DecisionMapper.to_outgoing_dtos(decisions)
        return result
    
    async def get_all(self) -> list[DecisionOutgoingDto]:
        async with AsyncSession(self.engine, autoflush=True, autocommit=False) as session:
            decisions: list[Decision] = await DecisionRepository(session).get_all()
            result=DecisionMapper.to_outgoing_dtos(decisions)
        return result