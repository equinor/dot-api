from fastapi import APIRouter, Depends, HTTPException
from src.dtos.graph_dtos import GraphIncomingDto, GraphOutgoingDto
from src.services.graph_service import GraphService
from src.dependencies import get_graph_service
from src.services.user_service import get_temp_user

router = APIRouter(tags=["graphs"])

@router.post("/graphs")
async def create_graphs(
    dtos: list[GraphIncomingDto],
    graph_service: GraphService = Depends(get_graph_service)
)-> list[GraphOutgoingDto]:
    try:
        user_dto=get_temp_user()
        return list(await graph_service.create(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/graphs/{id}")
async def get_graph(
    id: int,
    graph_service: GraphService = Depends(get_graph_service)
) -> GraphOutgoingDto:
    try:
        graphs: list[GraphOutgoingDto] = await graph_service.get([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if len(graphs) > 0:
        return graphs[0]
    else:
        raise HTTPException(status_code=404)
    
@router.get("/graphs")
async def get_all_graph(
    graph_service: GraphService = Depends(get_graph_service)
) -> list[GraphOutgoingDto]:
    try:
        graphs: list[GraphOutgoingDto] = await graph_service.get_all()
        return graphs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/graphs/{id}")
async def delete_graph(
    id: int,
    graph_service: GraphService = Depends(get_graph_service)
):
    try:
        await graph_service.delete([id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/graphs")
async def update_graphs(
    dtos: list[GraphIncomingDto],
    graph_service: GraphService = Depends(get_graph_service)
)-> list[GraphOutgoingDto]:
    try:
        user_dto=get_temp_user()
        return list(await graph_service.update(dtos, user_dto))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    