from fastapi import APIRouter, Depends, HTTPException
from src.services.user_service import (
    get_current_user, 
    UserService,
)
from src.dtos.user_dtos import (
    UserIncomingDto,
    UserOutgoingDto,
)
from src.dependencies import get_user_service

router = APIRouter(tags=["user"])

@router.get("/user/me")
async def get_me(
    current_user: UserIncomingDto = Depends(get_current_user)
) -> UserIncomingDto:
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")
    
@router.get("/users")
async def get_users(
    user_service: UserService = Depends(get_user_service),
) -> list[UserOutgoingDto]:
    try:
        return await user_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/users/{id}")
async def get_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
) -> UserOutgoingDto:
    try:
        result = await user_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(result) > 0:
        return result[0]
    else:
        raise HTTPException(status_code=404)

@router.get("/users/azure-id/{azure_id}")
async def get_user_by_azure_id(
    azure_id: str,
    user_service: UserService = Depends(get_user_service),
) -> UserOutgoingDto:
    try:
        result=await user_service.get_by_azure_id(azure_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        raise HTTPException(status_code=404)
    else:
        return result