from enum import Enum
from typing import Dict, Any, Tuple, List
from pydantic import BaseModel, validator , Field

import re
from datetime import datetime


class GenderEnum(int, Enum):
    GENDER_FEMALE = 1
    GENDER_MALE = 3
    GENDER_OTHER = 5
    GENDER_UNKNOWN = 7

class StatusEnum(int, Enum):
    STATUS_ENABLE = 1
    STATUS_DISABLED = 3

class customerBase(BaseModel):
    fullname: str  # Không sử dụng alias
    firstname: str
    lastname: str
    phone: str
    note: str
    gender: GenderEnum  # Sử dụng Enum để tự động xác thực
    status: StatusEnum = StatusEnum.STATUS_ENABLE  # Sử dụng Enum và giá trị mặc định từ enum

    @validator('phone')
    def validate_phone(cls, v):
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(v):
            raise ValueError('Invalid phone number format')
        return v

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class customerCreate(customerBase):
    pass

class customerUpdate(BaseModel):
    fullname: str  
    firstname: str
    lastname: str
    phone: str
    note: str
    gender: GenderEnum  
    status: StatusEnum 

    @validator('phone')
    def validate_phone(cls, v):
        if v is not None:
            phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
            if not phone_pattern.match(v):
                raise ValueError('Invalid phone number format')
        return v

    class Config:
        orm_mode = True
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

def preprocess_data(data):
    # Chuyển đổi JSON input để tương thích với các trường trong mô hình Pydantic
    return {
        "fullname": data.get("full_name"),
        "firstname": data.get("first_name"),
        "lastname": data.get("last_name"),
        "phone": data.get("phone"),
        "note": data.get("note"),
        "gender": data.get("gender"),
        "status": data.get("status", StatusEnum.STATUS_ENABLE)
    }

def validate_update_values(update_values: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []
    
    if "phone" in update_values:
        is_valid, error_msg = validate_phone(update_values['phone'])
        if not is_valid:
            errors.append(error_msg)
            
    if "fullname" in update_values:
        is_valid, error_msg = validate_fullname(update_values['fullname'])
        if not is_valid:
            errors.append(error_msg)
    
    # Validate cho các trường khác nếu cần

    return len(errors) == 0, errors

def validate_fullname(fullname: str) -> Tuple[bool, str]:
    if not fullname.replace(" ", "").isalpha():
        return False, 'Full name contains invalid characters'
    if len(fullname) > 100:
        return False, 'Full name is too long; must be 100 characters or less'
    return True, ''

def validate_phone(phone: str) -> Tuple[bool, str]:
    phone_pattern = re.compile(r'^\+?1?\d{9,15}\b')
    if not phone_pattern.match(phone):
        return False, 'Invalid phone number format'
    return True, ''
