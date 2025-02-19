from pydantic import BaseModel
from datetime import datetime

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