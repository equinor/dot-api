from fastapi import APIRouter, Depends, HTTPException
from src.dtos.node_dtos import NodeIncomingDto, NodeOutgoingDto
from src.services.node_service import NodeService
from src.dependencies import get_node_service
from src.services.user_service import get_temp_user


router = APIRouter(tags=["nodes"])

@router.post("/nodes")
async def create_nodes(
    dtos: list[NodeIncomingDto],
    node_service: NodeService = Depends(get_node_service)
)-> list[NodeOutgoingDto]:
    try:
        user_dto=get_temp_user()
        return list(await node_service.create(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nodes/{id}")
async def get_node(
    id: int,
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
    node_service: NodeService = Depends(get_node_service)
) -> list[NodeOutgoingDto]:
    try:
        nodes: list[NodeOutgoingDto] = await node_service.get_all()
        return nodes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/nodes/{id}")
async def delete_node(
    id: int,
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
        user_dto=get_temp_user()
        return list(await node_service.update(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    