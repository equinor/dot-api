import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession
from src.dtos.node_style_dtos import NodeStyleIncomingDto, NodeStyleOutgoingDto
from src.services.node_style_service import NodeStyleService
from src.dependencies import get_node_style_service
from src.constants import SwaggerDocumentationConstants
from src.dependencies import get_db


router = APIRouter(tags=["node_styles"])


@router.get("/node-styles/{id}")
async def get_node_style(
    id: uuid.UUID,
    node_style_service: NodeStyleService = Depends(get_node_style_service),
    session: AsyncSession = Depends(get_db),
) -> NodeStyleOutgoingDto:
    try:
        node_styles: list[NodeStyleOutgoingDto] = await node_style_service.get(session, [id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(node_styles) > 0:
        return node_styles[0]
    else:
        raise HTTPException(status_code=404)


@router.get("/node-styles")
async def get_all_node_style(
    node_style_service: NodeStyleService = Depends(get_node_style_service),
    filter: Optional[str] = Query(None, description=SwaggerDocumentationConstants.FILTER_DOC),
    session: AsyncSession = Depends(get_db),
) -> list[NodeStyleOutgoingDto]:
    try:
        node_styles: list[NodeStyleOutgoingDto] = await node_style_service.get_all(
            session, odata_query=filter
        )
        return node_styles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/node-styles/{id}")
async def delete_node_style(
    id: uuid.UUID,
    node_style_service: NodeStyleService = Depends(get_node_style_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await node_style_service.delete(session, [id])
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/node-styles")
async def delete_node_styles(
    ids: list[uuid.UUID] = Query([]),
    node_style_service: NodeStyleService = Depends(get_node_style_service),
    session: AsyncSession = Depends(get_db),
):
    try:
        await node_style_service.delete(session, ids)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/node-styles")
async def update_node_styles(
    dtos: list[NodeStyleIncomingDto],
    node_style_service: NodeStyleService = Depends(get_node_style_service),
    session: AsyncSession = Depends(get_db),
) -> list[NodeStyleOutgoingDto]:
    try:
        result = list(await node_style_service.update(session, dtos))
        await session.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
