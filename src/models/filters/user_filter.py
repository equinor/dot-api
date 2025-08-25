from typing import Optional
import uuid
from src.models.user import User
from src.models.filters.base_filter import BaseFilter
from sqlalchemy.sql import ColumnElement

class UserFilter(BaseFilter):
    ids: Optional[list[int]] = None
    names: Optional[list[str]] = None
    azure_ids: Optional[list[uuid.UUID]] = None

    def construct_filters(self) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []

        self.add_condition_for_property(self.ids, self._user_id_condition, conditions)
        self.add_condition_for_property(self.names, self._name_condition, conditions)
        self.add_condition_for_property(self.azure_ids, self._azure_id_condition, conditions)

        return conditions

    # Static helper methods to encapsulate condition logic
    @staticmethod
    def _user_id_condition(user_id: int) -> ColumnElement[bool]:
        return User.id == user_id

    @staticmethod
    def _name_condition(name: str) -> ColumnElement[bool]:
        return User.name.ilike(f"%{name}%")

    @staticmethod
    def _azure_id_condition(azure_id: uuid.UUID) -> ColumnElement[bool]:
        return User.azure_id == azure_id
