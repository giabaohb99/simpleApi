from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, MetaData
from sqlalchemy.sql import func

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, nullable=False),
    Column("age", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), nullable=True),  
    Column("status", Boolean, default=True)
)