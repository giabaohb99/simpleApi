from enum import Enum
from pydantic import BaseModel, validator
import re
from datetime import datetime
class customerBase(BaseModel):
    fullname: str
    firstname: str
    lastname: str
    phone: str
    note: str
    gender: int
    status: int


class GenderEnum(str, Enum):
    GENDER_FEMALE = 1
    GENDER_MALE = 3
    GENDER_OTHER = 5
    GENDER_UNKNOWN = 7

class StatusEnum(str, Enum):
    STATUS_ENABLE = 1
    STATUS_DISABLED = 3

class customerCreate(customerBase):
    @validator('phone')
    def validate_phone(cls, v):
        # Biểu thức chính quy để kiểm tra số điện thoại
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(v):
            raise ValueError('Invalid phone number format')
        return v

class customerUpdate(BaseModel):
    fullname: str = None
    firstname: str = None
    lastname: str = None
    phone: str = None
    note: str = None
    gender: int = None
    status: int = None

class customerInDB(customerBase):
    id: int
    created_at: int
    updated_at: int
    gender: int
    phone: str
    status: int

    class Config:
        orm_mode = True

class customerResponse(BaseModel):
    customer_id: int
    customer_full_name: str
    customer_first_name: str
    customer_lass_name: str
    phone: str
    note: str
    gender: int
    date_created: int
    date_updated: int
    status: int
    
# Hàm chuyển đổi
def getJsonData(customer: customerInDB) -> dict:
    return {
        "customer_id": customer.id,
        "customer_full_name": customer.fullname,
        "customer_first_name": customer.firstname,
        "customer_lass_name": customer.lastname,
        "phone": customer.phone,
        "note": customer.note,
        "gender": customer.gender,
        "date_created": customer.created_at,
        "date_updated": customer.updated_at,
        "status": customer.status
    }