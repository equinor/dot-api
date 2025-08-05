from typing import  Optional
from src.auth.auth import verify_token
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncEngine
from src.dtos.user_dtos import (
    UserMapper,
    UserIncomingDto,
    UserOutgoingDto,
)
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.services.session_handler import session_handler
from src.auth.graph_api import call_ms_graph_api

async def get_current_user(
    token: dict[str, str] = Depends(verify_token),
) -> UserIncomingDto:
    return await call_ms_graph_api(token)

class UserService:
    def __init__(self, engine: AsyncEngine):
        self.engine=engine

    async def get(self, ids: list[int]) -> list[UserOutgoingDto]:
        async with session_handler(self.engine) as session:
            users: list[User] = await UserRepository(session).get(ids)
            result=UserMapper.to_outgoing_dtos(users)
        return result
    
    async def get_all(self) -> list[UserOutgoingDto]:
        async with session_handler(self.engine) as session:
            users: list[User] = await UserRepository(session).get_all()
            result=UserMapper.to_outgoing_dtos(users)
        return result
    
    async def get_by_azure_id(self, azure_id: str) -> Optional[UserOutgoingDto]:
        async with session_handler(self.engine) as session:
            user: Optional[User] = await UserRepository(session).get_by_azure_id(azure_id)
            if user is None:
                return user
            else:
                result=UserMapper.to_outgoing_dto(user)
        return result