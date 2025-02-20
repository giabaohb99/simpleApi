from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, insert
from sqlalchemy.sql import func
from app.database import database

metadata = MetaData()

logs = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
    Column("action", String(50)),
    Column("source_type", String(50)),
    Column("source_id", Integer),
    Column("details", String),
    Column("ip_address", String(45)),
    Column("user_agent", String(255)) # Thêm cột này để lưu User-Agent
)

async def log_action(action: str, source_type: str, source_id: int, details: str, ip_address: str, user_agent: str):
    query = insert(logs).values(
        action=action,
        source_type=source_type,
        source_id=source_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent
    )
    await database.execute(query)