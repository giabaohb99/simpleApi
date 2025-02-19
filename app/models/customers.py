from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.sql import func
# from schemas.customers import StatusEnum

metadata = MetaData()


customer = Table(
    "customer",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("fullname", String, nullable=True),
    Column("firstname", String, nullable=True),
    Column("lastname", String, nullable=True),
    Column("phone", String, nullable=True),
    Column("note", String, nullable=True),
    Column("gender", Integer, nullable=True),
    Column("created_at", Integer, nullable=False),
    Column("updated_at", Integer, nullable=True),  
    Column("status", Integer, default=3)
)