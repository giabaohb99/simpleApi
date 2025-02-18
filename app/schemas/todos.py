from pydantic import BaseModel

class TodoBase(BaseModel):
    name: str
    description: str = None
    estimated_time: str = None
    status: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoInDB(TodoBase):
    id: int

    class Config:
        orm_mode = True