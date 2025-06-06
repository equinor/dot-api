from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.strategy_options import _AbstractLoad # type: ignore
from typing import Type, TypeVar, Generic, List, Protocol, Callable
from typing import List

LoadOptions = List[_AbstractLoad]

class AlchemyModel(Protocol):
    id: InstrumentedAttribute[int]

T = TypeVar('T', bound=AlchemyModel)

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T], query_extension_method: Callable[[], LoadOptions]):
        self.session = session
        self.model = model
        self.query_extension_method = query_extension_method

    async def create(self, entities: List[T]) -> List[T]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities
    
    async def create_single(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get(self, ids: List[int]) -> List[T]:
        query = select(self.model).where(self.model.id.in_(ids)).options(
            *self.query_extension_method()
        )
        return list((await self.session.scalars(query)).all())

    async def get_all(self) -> List[T]:
        query = select(self.model).options(
            *self.query_extension_method()
        )
        return list((await self.session.scalars(query)).all())

    async def delete(self, ids: List[int]) -> None:
        entities = await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()

    async def update(self, entities: List[T]) -> List[T]:
        raise NotImplementedError("Subclasses must implement update_entity method.")
