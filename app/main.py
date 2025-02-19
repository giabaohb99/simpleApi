from fastapi import FastAPI
from app.api import todos 
from app.database import database, engine
# from app.models.todos import metadata as todos_metadata
from app.models.users import metadata as users_metadata 
from app.models.logs import metadata as logs_metadata 
from app.models.customers import metadata as customers_metadata 
from app.api.users import router as users_router
from app.api.logs import router as logs_router
from app.api.customers import router as customers_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    # Kết hợp metadata từ tất cả các model và tạo bảng  
    # todos_metadata.create_all(engine)
    users_metadata.create_all(engine)
    logs_metadata.create_all(engine)
    customers_metadata.create_all(engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(users_router, prefix="/users", tags=["users"])
# app.include_router(todos_router, prefix="/todos", tags=["todos"])
app.include_router(logs_router, prefix="/logs", tags=["logs"])
app.include_router(customers_router, prefix="/customers", tags=["customers"])