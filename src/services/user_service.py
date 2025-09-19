from typing import Optional
from src.models.filters.user_filter import UserFilter
from src.auth.auth import verify_token
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.user_dtos import (
    UserMapper,
    UserIncomingDto,
    UserOutgoingDto,
)
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.auth.graph_api import call_ms_graph_api

async def get_current_user(
    token: str = Depends(verify_token),
) -> UserIncomingDto:
    return await call_ms_graph_api(token)

class UserService:
    async def get(self, session: AsyncSession, ids: list[int]) -> list[UserOutgoingDto]:
        users: list[User] = await UserRepository(session).get(ids)
        result = UserMapper.to_outgoing_dtos(users)
        return result

    async def get_all(self, session: AsyncSession, filter: Optional[UserFilter] = None, odata_query: Optional[str] = None) -> list[UserOutgoingDto]:
        model_filter = filter.construct_filters() if filter else []
        users: list[User] = await UserRepository(session).get_all(model_filter=model_filter, odata_query=odata_query)
        result = UserMapper.to_outgoing_dtos(users)
        return result
    
    async def get_by_azure_id(self, session: AsyncSession, azure_id: str) -> Optional[UserOutgoingDto]:
        user: Optional[User] = await UserRepository(session).get_by_azure_id(azure_id)
        if user is None:
            return user
        else:
            result = UserMapper.to_outgoing_dto(user)
        return result
