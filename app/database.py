from sqlalchemy import create_engine, MetaData
from databases import Database
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql://username:password@db:5432/todos"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

@asynccontextmanager
async def transaction_context():
    async with database.transaction() as transaction:
        yield transaction