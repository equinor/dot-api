from typing import Optional, List, Callable, TypeVar
from pydantic import BaseModel
from sqlalchemy.sql import and_, or_, ColumnElement
from sqlalchemy.sql._typing import _ColumnExpressionArgument  # type: ignore

T = TypeVar("T")


class BaseFilter(BaseModel):
    @staticmethod
    def combine_conditions(
        conditions: List[_ColumnExpressionArgument[bool]], use_and: bool = True
    ) -> ColumnElement[bool]:
        return and_(*conditions) if use_and else or_(*conditions)

    @staticmethod
    def add_condition(
        conditions: List[_ColumnExpressionArgument[bool]],
        condition: Optional[_ColumnExpressionArgument[bool]],
    ) -> None:
        if condition is not None:
            conditions.append(condition)

    @staticmethod
    def add_condition_for_property(
        attribute: Optional[list[T]],
        condition_func: Callable[[T], ColumnElement[bool]],
        conditions: list[ColumnElement[bool]],
    ) -> None:
        if attribute:
            conditions.append(or_(*[condition_func(value) for value in attribute]))
