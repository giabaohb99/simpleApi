from fastapi import APIRouter, HTTPException, Query , Request
from app.schemas.users import UserCreate, UserUpdate, UserInDB
from app.services.users import (
    create_user_logic,
    get_user_logic,
    list_users_logic,
    update_user_logic,
    delete_user_logic
)

router = APIRouter()

@router.post("/", response_model=UserInDB)
async def create_user(user: UserCreate , request: Request):
    return await create_user_logic(user,request)

@router.get("/{user_id}", response_model=UserInDB)
async def get_user(user_id: int):
    return await get_user_logic(user_id)

@router.get("/", response_model=dict)
async def list_users(
    status: bool = None, name: str = None, age_from: int = None, age_to: int = None,
    date_created_from: str = None, date_created_to: str = None, user_id: int = None,
    page: int = Query(1, ge=1), limit: int = Query(10, ge=1)
):
    return await list_users_logic(status, name, age_from, age_to, date_created_from, date_created_to, user_id, page, limit)

@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: int, user_update: UserUpdate , request: Request):
    return await update_user_logic(user_id, user_update,request)

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    return await delete_user_logic(user_id)