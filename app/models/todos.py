from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, text

metadata = MetaData()

todos = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("estimated_time", String),
    Column("status", Boolean, server_default=text("false")),
)