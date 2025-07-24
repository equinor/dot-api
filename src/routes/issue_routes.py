import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.dtos.issue_dtos import IssueIncomingDto, IssueOutgoingDto
from src.services.issue_service import IssueService
from src.dependencies import get_issue_service
from src.services.user_service import get_temp_user
from src.models.filters.issues_filter import IssueFilter


router = APIRouter(tags=["issues"])

@router.post("/issues")
async def create_issues(
    dtos: list[IssueIncomingDto],
    issue_service: IssueService = Depends(get_issue_service)
)-> list[IssueOutgoingDto]:
    """
    Endpoint for creating Issues. 
    If supplied with nodes/decisions/uncertainties they will be created after the issue with the appropriate Id.
    If node is not supplied an empty node will be created
    """
    try:
        user_dto=get_temp_user()
        return list(await issue_service.create(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/issues/{id}")
async def get_issue(
    id: uuid.UUID,
    issue_service: IssueService = Depends(get_issue_service)
) -> IssueOutgoingDto:
    try:
        issues: list[IssueOutgoingDto] = await issue_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(issues) > 0:
        return issues[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/issues")
async def get_all_issue(
    issue_service: IssueService = Depends(get_issue_service),
    filter: Optional[str] = Query(None),
) -> list[IssueOutgoingDto]:
    try:
        issues: list[IssueOutgoingDto] = await issue_service.get_all(odata_query=filter)
        return issues
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/projects/{project_id}/issues")
async def get_all_issues_from_project(
    project_id: uuid.UUID,
    issue_service: IssueService = Depends(get_issue_service),
    filter: Optional[str] = Query(None),
) -> list[IssueOutgoingDto]:
    try:
        issues: list[IssueOutgoingDto] = await issue_service.get_all(IssueFilter(project_id=project_id), odata_query=filter)
        return issues
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/scenarios/{scenario_id}/issues")
async def get_all_issues_from_scenario(
    scenario_id: uuid.UUID,
    issue_service: IssueService = Depends(get_issue_service),
    filter: Optional[str] = Query(None),
) -> list[IssueOutgoingDto]:
    try:
        issues: list[IssueOutgoingDto] = await issue_service.get_all(IssueFilter(scenario_id=scenario_id), odata_query=filter)
        return issues
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/issues/{id}")
async def delete_issue(
    id: uuid.UUID,
    issue_service: IssueService = Depends(get_issue_service)
):
    try:
        await issue_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/issues")
async def update_issues(
    dtos: list[IssueIncomingDto],
    issue_service: IssueService = Depends(get_issue_service)
)-> list[IssueOutgoingDto]:
    try:
        user_dto=get_temp_user()
        return list(await issue_service.update(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    