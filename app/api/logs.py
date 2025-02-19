from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from app.database import database
from app.models.logs import logs
from app.schemas.logs import LogInDB
from app.services.logs import list_logs_logic
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=dict)
async def get_logs(
    start_date: str = None,
    end_date: str = None,
    source_id: int = None,
    source_type: str = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    return await list_logs_logic(
        start_date=start_date,
        end_date=end_date,
        source_id=source_id,
        source_type=source_type,
        page=page,
        limit=limit
    )