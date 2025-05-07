from src.models import Decision
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class DecisionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, decisions: list[Decision]) -> list[Decision]:
        self.session.add_all(decisions)
        await self.session.flush()
        return decisions

    async def retrieve(self, ids: list[int]) -> list[Decision]:
        return list(
            (await self.session.scalars(select(Decision).where(Decision.id.in_(ids)))).all()
        )
    
