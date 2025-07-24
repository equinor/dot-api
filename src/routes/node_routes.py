import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from src.dtos.node_dtos import NodeIncomingDto, NodeOutgoingDto
from src.services.node_service import NodeService
from src.dependencies import get_node_service
from src.models.filters.node_filter import NodeFilter
from src.constants import SwaggerDocumentationConstants

router = APIRouter(tags=["nodes"])

@router.get("/nodes/{id}")
async def get_node(
    id: uuid.UUID,
    node_service: NodeService = Depends(get_node_service)
) -> NodeOutgoingDto:
    try:
        nodes: list[NodeOutgoingDto] = await node_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(nodes) > 0:
        return nodes[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/nodes")
async def get_all_node(
    node_service: NodeService = Depends(get_node_service),
    filter: Optional[str]=Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
) -> list[NodeOutgoingDto]:
    try:
        nodes: list[NodeOutgoingDto] = await node_service.get_all(odata_query=filter)
        return nodes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/projects/{project_id}/nodes")
async def get_all_nodes_from_project(
    project_id: uuid.UUID,
    issue_service: NodeService = Depends(get_node_service),
    filter: Optional[str]=Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
) -> list[NodeOutgoingDto]:
    try:
        issues: list[NodeOutgoingDto] = await issue_service.get_all(NodeFilter(project_id=project_id), odata_query=filter)
        return issues
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/scenarios/{scenario_id}/nodes")
async def get_all_nodes_from_scenario(
    scenario_id: uuid.UUID,
    issue_service: NodeService = Depends(get_node_service),
    filter: Optional[str]=Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
) -> list[NodeOutgoingDto]:
    try:
        issues: list[NodeOutgoingDto] = await issue_service.get_all(NodeFilter(scenario_id=scenario_id), odata_query=filter)
        return issues
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/nodes/{id}")
async def delete_node(
    id: uuid.UUID,
    node_service: NodeService = Depends(get_node_service)
):
    try:
        await node_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/nodes")
async def update_nodes(
    dtos: list[NodeIncomingDto],
    node_service: NodeService = Depends(get_node_service)
)-> list[NodeOutgoingDto]:
    try:
        return list(await node_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    