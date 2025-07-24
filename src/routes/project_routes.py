import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.dtos.project_dtos import (
    ProjectIncomingDto, 
    ProjectOutgoingDto, 
    ProjectCreateDto,
    PopulatedProjectDto,
)
from src.services.project_service import ProjectService
from src.dependencies import get_project_service
from src.services.user_service import get_temp_user

router = APIRouter(tags=["projects"])

@router.post("/projects")
async def create_projects(
    dtos: list[ProjectCreateDto],
    project_service: ProjectService = Depends(get_project_service)
)-> list[ProjectOutgoingDto]:
    """
    Endpoint for creating Projects.
    A Scenario must be supplied and will be created after the Project with the appropriate Id.
    If Objectives/Opportunities are supplied with the Scenario, then they will be created after the Scenario with the appropriate Id.
    """
    try:
        user_dto=get_temp_user()
        return list(await project_service.create(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{id}")
async def get_project(
    id: uuid.UUID,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectOutgoingDto:
    try:
        projects: list[ProjectOutgoingDto] = await project_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(projects) > 0:
        return projects[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/projects-populated/{id}")
async def get_populated_project(
    id: uuid.UUID,
    project_service: ProjectService = Depends(get_project_service),
) -> PopulatedProjectDto:
    try:
        projects: list[PopulatedProjectDto] = await project_service.get_populated_projects([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(projects) > 0:
        return projects[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/projects-populated")
async def get_all_populated_project(
    project_service: ProjectService = Depends(get_project_service),
    filter: Optional[str]=Query(None),
) -> list[PopulatedProjectDto]:
    try:
        projects: list[PopulatedProjectDto] = await project_service.get_all_populated_projects(odata_query=filter)
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/projects")
async def get_all_project(
    project_service: ProjectService = Depends(get_project_service),
    filter: Optional[str]=Query(None),
) -> list[ProjectOutgoingDto]:
    try:
        projects: list[ProjectOutgoingDto] = await project_service.get_all(odata_query=filter)
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/projects/{id}")
async def delete_project(
    id: uuid.UUID,
    project_service: ProjectService = Depends(get_project_service)
):
    try:
        await project_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/projects")
async def update_projects(
    dtos: list[ProjectIncomingDto],
    project_service: ProjectService = Depends(get_project_service)
)-> list[ProjectOutgoingDto]:
    try:
        user_dto=get_temp_user()
        return list(await project_service.update(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    