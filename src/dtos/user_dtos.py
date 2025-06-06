from pydantic import BaseModel, Field
from typing import Optional, Annotated
from src.models.user import (
    User
)
from src.constants import DatabaseConstants

class UserDto(BaseModel):
    name: Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)]
    azure_id: Annotated[str, Field(max_length=DatabaseConstants.MAX_SHORT_STRING_LENGTH.value)]

class UserIncomingDto(UserDto):
    id: Optional[int]

class UserOutgoingDto(UserDto):
    id: int

class UserMapper:
    @staticmethod
    def to_outgoing_dto(entity: User) -> UserOutgoingDto:
        return UserOutgoingDto(
            id=entity.id,
            name=entity.name,
            azure_id=entity.azure_id
        )         

    @staticmethod
    def to_entity(dto: UserIncomingDto) -> User:
        return User(
            id=dto.id,
            name=dto.name,
            azure_id=dto.azure_id
        )
    
    @staticmethod
    def to_outgoing_dtos(entities: list[User]) -> list[UserOutgoingDto]:
        return [UserMapper.to_outgoing_dto(entity) for entity in entities]
    
    @staticmethod
    def to_entities(dtos: list[UserIncomingDto]) -> list[User]:
        return [UserMapper.to_entity(dto) for dto in dtos]