from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData
from sqlalchemy.sql import func

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