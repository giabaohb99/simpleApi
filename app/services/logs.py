from sqlalchemy import select
from app.database import database
from app.models.logs import logs
from app.schemas.logs import LogInDB
from datetime import datetime

async def list_logs_logic(
    start_date: str = None,
    end_date: str = None,
    source_id: int = None,
    source_type: str = None,
    page: int = 1,
    limit: int = 10
) -> dict:
    offset = (page - 1) * limit
    query = select(logs)

    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.where(logs.c.timestamp >= start_datetime)
    
    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.where(logs.c.timestamp <= end_datetime)
    
    if source_id is not None:
        query = query.where(logs.c.source_id == source_id)
    
    if source_type:
        query = query.where(logs.c.source_type == source_type)
    
    query = query.offset(offset).limit(limit)
    log_list = await database.fetch_all(query)
    
    return {
        "total": len(log_list),
        "currentpage": page,
        "limit": limit,
        "items": [LogInDB(**log) for log in log_list]
    }