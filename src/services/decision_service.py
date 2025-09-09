import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.decision import Decision
from src.dtos.decision_dtos import (
    DecisionIncomingDto, 
    DecisionOutgoingDto, 
    DecisionMapper
)
from src.repositories.decision_repository import DecisionRepository

class DecisionService:
    async def create(self, session: AsyncSession, dtos: list[DecisionIncomingDto]) -> list[DecisionOutgoingDto]:
        entities: list[Decision] = await DecisionRepository(session).create(DecisionMapper.to_entities(dtos))
        # get the dtos while the entities are still connected to the session
        result: list[DecisionOutgoingDto] = DecisionMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, session: AsyncSession, dtos: list[DecisionIncomingDto]) -> list[DecisionOutgoingDto]:
        entities: list[Decision] = await DecisionRepository(session).update(DecisionMapper.to_entities(dtos))
        # get the dtos while the entities are still connected to the session
        result: list[DecisionOutgoingDto] = DecisionMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, session: AsyncSession, ids: list[uuid.UUID]):
        await DecisionRepository(session).delete(ids)
    
    async def get(self, session: AsyncSession, ids: list[uuid.UUID]) -> list[DecisionOutgoingDto]:
        decisions: list[Decision] = await DecisionRepository(session).get(ids)
        result=DecisionMapper.to_outgoing_dtos(decisions)
        return result
    
    async def get_all(self, session: AsyncSession, odata_query: Optional[str]=None) -> list[DecisionOutgoingDto]:
        decisions: list[Decision] = await DecisionRepository(session).get_all(odata_query=odata_query)
        result=DecisionMapper.to_outgoing_dtos(decisions)
        return result
