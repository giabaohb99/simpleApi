from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class ActionEnum(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class SourceTypeEnum(str, Enum):
    USER = "user"
    TODO = "todo"


class LogBase(BaseModel):
    action: str
    source_type: str
    source_id: int
    details: str
    ip_address: str

class LogCreate(LogBase):
    pass

class LogInDB(LogBase):
    id: int
    timestamp: datetime
