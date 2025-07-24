from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import ColumnElement, Select, select
from sqlalchemy.orm.strategy_options import _AbstractLoad # type: ignore
from typing import Type, TypeVar, Generic, List, Protocol, Callable, Union, Optional, Tuple, cast
from odata_query.sqlalchemy.shorthand import apply_odata_query
import uuid

LoadOptions = List[_AbstractLoad]

class AlchemyModel(Protocol):
    id: InstrumentedAttribute[Union[int, uuid.UUID]]

T = TypeVar('T', bound=AlchemyModel)
IDType = TypeVar('IDType', int, uuid.UUID)

class BaseRepository(Generic[T, IDType]):
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

    async def get(self, ids: List[IDType]) -> List[T]:
        query = select(self.model).where(self.model.id.in_(ids)).options(
            *self.query_extension_method()
        )
        return list((await self.session.scalars(query)).all())

    async def get_all(self, model_filter: Optional[ColumnElement[bool]]=None, odata_query: Optional[str]=None) -> List[T]:
        query = select(self.model).options(
            *self.query_extension_method()
        )
        if model_filter is not None:
            query=query.filter(model_filter)
        if odata_query is not None:
            query = cast(Select[Tuple[T]], apply_odata_query(query, odata_query))
        return list((await self.session.scalars(query)).all())

    async def delete(self, ids: List[IDType]) -> None:
        entities = await self.get(ids)
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()

    async def update(self, entities: List[T]) -> List[T]:
        raise NotImplementedError("Subclasses must implement update_entity method.")
