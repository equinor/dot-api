import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.dtos.issue_dtos import IssueOutgoingDto
from src.services.structure_service import StructureService
from src.dependencies import get_structure_service
from src.models.filters.issues_filter import IssueFilter
from src.constants import SwaggerDocumentationConstants

router = APIRouter(tags=["structure"])


@router.get("/structure/{scenario_id}")
async def get_decision_tree(
    scenario_id: uuid.UUID,
    structure_service: StructureService = Depends(get_structure_service)
) -> list[IssueOutgoingDto]:
    try:
        issues: list[IssueOutgoingDto] = await structure_service.create_decision_tree(scenario_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(issues) > 0:
        return issues
    else:
        raise HTTPException(status_code=404)
    

@router.get("/structure/{scenario_id}/ID")
async def read_influence_diagram(
    scenario_id: uuid.UUID,
    structure_service: StructureService = Depends(get_structure_service)
) -> list[IssueOutgoingDto]:
    try:
        issues: list[IssueOutgoingDto] = await structure_service.read_influence_diagram(scenario_id)
        #return issues
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(issues) > 0:
        return issues
    else:
        raise HTTPException(status_code=404)
    



    