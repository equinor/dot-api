from fastapi import APIRouter, Depends, HTTPException
from src.dtos.edge_dtos import *
from src.services.edge_service import EdgeService
from src.dependencies import get_edge_service

router = APIRouter(tags=["edges"])

@router.post("/edges")
async def create_edges(
    dtos: list[EdgeIncomingDto],
    edge_service: EdgeService = Depends(get_edge_service)
)-> list[EdgeOutgoingDto]:
    try:
        return list(await edge_service.create(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/edges/{id}")
async def get_edge(
    id: int,
    edge_service: EdgeService = Depends(get_edge_service)
) -> EdgeOutgoingDto:
    try:
        edges: list[EdgeOutgoingDto] = await edge_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(edges) > 0:
        return edges[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/edges")
async def get_all_edge(
    edge_service: EdgeService = Depends(get_edge_service)
) -> list[EdgeOutgoingDto]:
    try:
        edges: list[EdgeOutgoingDto] = await edge_service.get_all()
        return edges
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/edges/{id}")
async def delete_edge(
    id: int,
    edge_service: EdgeService = Depends(get_edge_service)
):
    try:
        await edge_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/edges")
async def update_edges(
    dtos: list[EdgeIncomingDto],
    edge_service: EdgeService = Depends(get_edge_service)
)-> list[EdgeOutgoingDto]:
    try:
        return list(await edge_service.update(dtos))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    