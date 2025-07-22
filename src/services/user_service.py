from typing import cast, Optional
from src.dtos.user_dtos import UserIncomingDto
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

async def get_current_user(
    claims: dict[str, str] = Depends(verify_token),
) -> UserIncomingDto:
        if claims.get("name") is not None and claims.get("oid") is not None:
            name: str = cast(str, claims.get("name"))
            upn: str = cast(str, claims.get("oid"))
        else:
            raise ValueError("Invalid claims: 'name' or 'oid' is missing")
            
        return UserIncomingDto(
            id=None,
            name=name,
            azure_id=upn
        )
        
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