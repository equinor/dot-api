import uuid
from sqlalchemy.ext.asyncio import AsyncEngine
from src.models.decision import Decision
from src.dtos.decision_dtos import (
    DecisionIncomingDto, 
    DecisionOutgoingDto, 
    DecisionMapper
)
from src.repositories.decision_repository import DecisionRepository
from src.services.session_handler import session_handler

class DecisionService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def create(self, dtos: list[DecisionIncomingDto]) -> list[DecisionOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Decision] = await DecisionRepository(session).create(DecisionMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[DecisionOutgoingDto] = DecisionMapper.to_outgoing_dtos(entities)
        return result
    
    async def update(self, dtos: list[DecisionIncomingDto]) -> list[DecisionOutgoingDto]:
        async with session_handler(self.engine) as session:
            entities: list[Decision] = await DecisionRepository(session).update(DecisionMapper.to_entities(dtos))
            # get the dtos while the entities are still connected to the session
            result: list[DecisionOutgoingDto] = DecisionMapper.to_outgoing_dtos(entities)
        return result
    
    async def delete(self, ids: list[uuid.UUID]):
        async with session_handler(self.engine) as session:
            await DecisionRepository(session).delete(ids)
    
    async def get(self, ids: list[uuid.UUID]) -> list[DecisionOutgoingDto]:
        async with session_handler(self.engine) as session:
            decisions: list[Decision] = await DecisionRepository(session).get(ids)
            result=DecisionMapper.to_outgoing_dtos(decisions)
        return result
    
    async def get_all(self) -> list[DecisionOutgoingDto]:
        async with session_handler(self.engine) as session:
            decisions: list[Decision] = await DecisionRepository(session).get_all()
            result=DecisionMapper.to_outgoing_dtos(decisions)
        return result