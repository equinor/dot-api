import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.edge_dtos import (
    EdgeIncomingDto,
    EdgeOutgoingDto,
)
from src.services.edge_service import EdgeService
from src.dependencies import get_edge_service
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_db
from src.utils.session_commit import commit_if_changed_async

router = APIRouter(tags=["edges"])


@router.post("/edges")
async def create_edges(
    dtos: list[EdgeIncomingDto],
    edge_service: EdgeService = Depends(get_edge_service),
    session: AsyncSession = Depends(get_db),
) -> list[EdgeOutgoingDto]:
    try:
        result = list(await edge_service.create(session, dtos))
        await commit_if_changed_async(session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/edges/{id}")
async def get_edge(
    id: uuid.UUID,
    edge_service: EdgeService = Depends(get_edge_service),
    session: AsyncSession = Depends(get_db),
) -> EdgeOutgoingDto:
    try:
        edges: list[EdgeOutgoingDto] = await edge_service.get(session, [id])
        await commit_if_changed_async(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(edges) > 0:
        return edges[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/edges")
async def get_all_edge(
    edge_service: EdgeService = Depends(get_edge_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[EdgeOutgoingDto]:
    try:
        edges: list[EdgeOutgoingDto] = await edge_service.get_all(session, odata_query=filter)
        return edges
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/edges/{id}")
async def delete_edge(
    id: uuid.UUID,
    edge_service: EdgeService = Depends(get_edge_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await edge_service.delete(session, [id])
        await commit_if_changed_async(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/edges")
async def delete_edges(
    ids: list[uuid.UUID] = Query([]),
    edge_service: EdgeService = Depends(get_edge_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await edge_service.delete(session, ids)
        await commit_if_changed_async(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/edges")
async def update_edges(
    dtos: list[EdgeIncomingDto],
    edge_service: EdgeService = Depends(get_edge_service),
    session: AsyncSession = Depends(get_db),
) -> list[EdgeOutgoingDto]:
    try:
        result = list(await edge_service.update(session, dtos))
        await commit_if_changed_async(session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
