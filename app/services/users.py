from urllib import request
from sqlalchemy import func, select, insert, update, delete
from app.database import database
from app.models.users import users
from app.schemas.users import UserCreate, UserUpdate, UserInDB ,getJsonData
from app.models.logs import logs , log_action
from app.schemas.logs import ActionEnum, SourceTypeEnum
from datetime import datetime
from fastapi import HTTPException, Request

async def create_user_logic(user: UserCreate , request: Request) -> UserInDB:
    if user.age < 0:
        raise HTTPException(status_code=400, detail="Age cannot be negative")
    query = insert(users).values(
        name=user.name,
        age=user.age,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        status=True
    )
    user_id = await database.execute(query)
    new_user = await get_user_logic(user_id)
    await log_action(
        action=ActionEnum.CREATE,
        source_type=SourceTypeEnum.USER,
        source_id=user_id,
        details=f"User {user.name} created",
        ip_address=request.client.host,
        user_agent = request.headers.get('User-Agent', 'unknown')
    )
    return getJsonData(new_user)


async def get_user_logic(user_id: int) -> UserInDB:
    query = select(users).where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if not user:
        error_response = create_error_response(404, "User not found")
        raise HTTPException(status_code=404, detail=error_response)
    return UserInDB(**user)

async def list_users_logic(
    status: bool = None, name: str = None, age_from: int = None, age_to: int = None,
    date_created_from: str = None, date_created_to: str = None, user_id: int = None,
    page: int = 1, limit: int = 10
) -> dict:
    offset = (page - 1) * limit
    query = select(users)
    if status is not None:
        query = query.where(users.c.status == status)
    if name:
        query = query.where(users.c.name.ilike(f"%{name}%"))
    if age_from is not None:
        query = query.where(users.c.age >= age_from)
    if age_to is not None:
        query = query.where(users.c.age <= age_to)
    if date_created_from:
        date_from = datetime.strptime(date_created_from, "%Y-%m-%d")
        query = query.where(users.c.created_at >= date_from)
    if date_created_to:
        date_to = datetime.strptime(date_created_to, "%Y-%m-%d")
        query = query.where(users.c.created_at <= date_to)
    if user_id:
        query = query.where(users.c.id == user_id)
    total_query = select(func.count()).select_from(query.alias('subquery'))
    total = await database.fetch_val(total_query)
    query = query.offset(offset).limit(limit)
    user_list = await database.fetch_all(query)
    return {
        "total": total,
        "currentpage": page,
        "limit": limit,
        "items": [UserInDB(**user) for user in user_list]
    }

async def update_user_logic(user_id: int, user_update: UserUpdate, request: Request) -> UserInDB:
    current_user_query = select(users).where(users.c.id == user_id)
    current_user = await database.fetch_one(current_user_query)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_values = user_update.dict(exclude_unset=True)
    updated_values["updated_at"] = datetime.utcnow()
    query = update(users).where(users.c.id == user_id).values(**updated_values)
    await database.execute(query)

    # Ghi log cho hành động update
    await log_action(
        action=ActionEnum.CREATE,
        source_type=SourceTypeEnum.USER,
        source_id=user_id,
        details=f"User {current_user['name']} updated",
        ip_address=request.client.host,
        user_agent = request.headers.get('User-Agent', 'unknown')
    )

    myUser =  await get_user_logic(user_id)
    return getJsonData(myUser)


async def delete_user_logic(user_id: int) -> dict:
    user_query = select(users).where(users.c.id == user_id)
    user = await database.fetch_one(user_query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    query = delete(users).where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted successfully"}



def create_error_response(status_code: int, message: str):
    return {"error": {"status_code": status_code, "message": message}}
