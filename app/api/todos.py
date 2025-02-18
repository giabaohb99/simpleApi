from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, insert, update, delete, and_, or_, func
from app.database import database
from app.models.todos import todos
from app.schemas.todos import TodoCreate, TodoUpdate, TodoInDB

router = APIRouter()

@router.get("/", response_model=dict)
async def read_todos(
    page: int = 1,
    limit: int = 50,
    date: str = Query(None, alias="date"),
    keyword: str = Query(None, alias="keyword"),
    status: bool = Query(None, alias="status")
):
    # Tính toán offset
    offset = (page - 1) * limit

    base_query = select(todos)

    # Thêm điều kiện lọc nếu có
    if date:
        base_query = base_query.where(todos.c.estimated_time == date)
    
    if keyword:
        base_query = base_query.where(or_(todos.c.name.ilike(f"%{keyword}%"), todos.c.description.ilike(f"%{keyword}%")))

    if status is not None:
        base_query = base_query.where(todos.c.status == status)

    # Tính tổng số các bản ghi không bị ảnh hưởng bởi phân trang
    total_query = select(func.count()).select_from(base_query.alias('subquery'))
    total = await database.fetch_val(total_query)

    # Thêm phân trang
    result_query = base_query.offset(offset).limit(limit).order_by(todos.c.id.desc())
    results = await database.fetch_all(result_query)
    return {
        "total": total,
        "currentpage": page,
        "limit": limit,
        "items": (dict(result) for result in results)
    }

@router.post("/", response_model=TodoInDB)
async def create_todo(todo: TodoCreate):
    query = insert(todos).values(todo.dict())
    last_record_id = await database.execute(query)
    return TodoInDB(**todo.dict(), id=last_record_id)

@router.put("/{todo_id}", response_model=TodoInDB)
async def update_todo(todo_id: int, todo: TodoUpdate):
    # Kiểm tra sự tồn tại của bản ghi trước khi cập nhật
    existing_record = await database.fetch_one(select(todos).where(todos.c.id == todo_id))
    if not existing_record:
        raise HTTPException(status_code=404, detail="Todo not found")

    query = update(todos).where(todos.c.id == todo_id).values(todo.dict())
    await database.execute(query)
    return {**todo.dict(), "id": todo_id}

@router.delete("/{todo_id}", response_model=dict)
async def delete_todo(todo_id: int):
    # Kiểm tra sự tồn tại của bản ghi trước khi xoá
    existing_record = await database.fetch_one(select(todos).where(todos.c.id == todo_id))
    if not existing_record:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    query = delete(todos).where(todos.c.id == todo_id)
    await database.execute(query)
    return {"message": "Todo deleted"}