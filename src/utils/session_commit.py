from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

async def commit_if_changed_async(session: AsyncSession):
    if session.dirty or session.new or session.deleted: await session.commit()

def commit_if_changed(session: Session):
    if session.dirty or session.new or session.deleted: session.commit()
