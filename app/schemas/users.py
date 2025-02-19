from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    age: int


class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str = None
    age: int = None
    status: bool = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    status: bool

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    age: int
    date_created: datetime
    date_updated: datetime
    status: bool
    
# Hàm chuyển đổi
def getJsonData(user_in_db: UserInDB) -> dict:
    return {
        "user_id": user_in_db.id,
        "user_name": user_in_db.name,
        "age": user_in_db.age,
        "date_created": user_in_db.created_at.isoformat(),
        "date_updated": user_in_db.updated_at.isoformat(),
        "status": user_in_db.status
    }