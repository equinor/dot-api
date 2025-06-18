import uuid
from fastapi import APIRouter, Depends, HTTPException
from src.dtos.node_style_dtos import NodeStyleIncomingDto, NodeStyleOutgoingDto
from src.services.node_style_service import NodeStyleService
from src.dependencies import get_node_style_service

router = APIRouter(tags=["node_styles"])

@router.get("/node-styles/{id}")
async def get_node_style(
    id: uuid.UUID,
    node_style_service: NodeStyleService = Depends(get_node_style_service)
) -> NodeStyleOutgoingDto:
    try:
        node_styles: list[NodeStyleOutgoingDto] = await node_style_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(node_styles) > 0:
        return node_styles[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/node-styles")
async def get_all_node_style(
    node_style_service: NodeStyleService = Depends(get_node_style_service)
) -> list[NodeStyleOutgoingDto]:
    try:
        node_styles: list[NodeStyleOutgoingDto] = await node_style_service.get_all()
        return node_styles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/node-styles/{id}")
async def delete_node_style(
    id: uuid.UUID,
    node_style_service: NodeStyleService = Depends(get_node_style_service)
):
    try:
        await node_style_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/node-styles")
async def update_node_styles(
    dtos: list[NodeStyleIncomingDto],
    node_style_service: NodeStyleService = Depends(get_node_style_service)
)-> list[NodeStyleOutgoingDto]:
    try:
        return list(await node_style_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    