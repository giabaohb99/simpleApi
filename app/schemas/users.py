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