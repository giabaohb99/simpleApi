from urllib import request
from pydantic import ValidationError
from typing import Optional
from sqlalchemy import func, select, insert, update, delete
from app.database import database , transaction_context
from app.models.customers import customer
from app.schemas.customers import customerCreate, customerUpdate, customerInDB ,GenderEnum ,StatusEnum,getJsonData , preprocess_data, validate_update_values
from app.models.logs import logs , log_action
from app.schemas.logs import ActionEnum, SourceTypeEnum 
from datetime import datetime
from fastapi import HTTPException, Request
from app.errors import raise_custom_http_exception
import time


async def addCustomers(request: Request) -> customerInDB:
    async with transaction_context() as transaction:
        try:
            raw_data = await request.json()
            processed_data = preprocess_data(raw_data)
            try:
                customer_data = customerCreate(**processed_data)
            except ValidationError as e:
                raise_custom_http_exception(422, str(e))
            query = select(customer).where(customer.c.phone == customer_data.phone)
            existing_customer = await database.fetch_one(query)
            
            if existing_customer:
                raise_custom_http_exception(422, 'error_phone_exists')
            
            timeday = time.time()
            query = insert(customer).values(
                fullname=customer_data.fullname,
                firstname=customer_data.firstname,
                lastname=customer_data.lastname,
                gender=customer_data.gender,  
                phone=customer_data.phone,
                note=customer_data.note,
                created_at=int(timeday),
                updated_at=int(timeday),
                status=customer_data.status,  
            )
            addCustomer = await database.execute(query)
            newCustomer = await getDetailCustomer(addCustomer)
            if newCustomer is None:
                raise_custom_http_exception(422, 'error_customer_id_invaid')
                
            # Optional logging
            await log_action(
                action=ActionEnum.CREATE,
                source_type=SourceTypeEnum.CUSTOMER,
                source_id=addCustomer,
                details=f"customer {customer_data.fullname} created",
                ip_address=request.client.host,
                user_agent=request.headers.get('User-Agent', 'unknown')
            )
            
            return getJsonData(newCustomer)
        except Exception as e:
            await transaction.rollback()
            raise_custom_http_exception(500, "Internal server error")
    


async def getDetailCustomer(customer_id: int) -> customerInDB:
    query = select(customer).where(customer.c.id == customer_id)
    result = await database.fetch_one(query)
    if not result:
        error_response = create_error_response(404, "User not found")
        raise HTTPException(status_code=404, detail=error_response)
    return customerInDB(**result)

async def listCustomers(
    fullname: Optional[str] = None, gender: Optional[GenderEnum] = None, 
    status: Optional[StatusEnum] = None,
    date_created_from: Optional[str] = None, date_created_to: Optional[str] = None, 
    customer_id: Optional[int] = None,
    page: int = 1, limit: int = 10
) -> dict:
    offset = (page - 1) * limit
    query = select(customer)
    
    if fullname:
        query = query.where(customer.c.fullname.ilike(f"%{fullname}%"))
    if gender is not None:
        query = query.where(customer.c.gender == gender.value)
    if status is not None:
        query = query.where(customer.c.status == status.value)
    if date_created_from:
        date_from = datetime.strptime(date_created_from, "%Y-%m-%d")
        query = query.where(customer.c.created_at >= date_from)
    if date_created_to:
        date_to = datetime.strptime(date_created_to, "%Y-%m-%d")
        query = query.where(customer.c.created_at <= date_to)
    if customer_id:
        query = query.where(customer.c.id == customer_id)
    
    # Tính tổng số bản ghi khớp với bộ lọc
    total_query = select(func.count()).select_from(query.alias('subquery'))
    total = await database.fetch_val(total_query)
    
    # Sử dụng offset và limit cho phân trang
    query = query.offset(offset).limit(limit)
    
    # Thực hiện truy vấn và xử lý kết quả
    customer_list = await database.fetch_all(query)
    
    return {
        "total": total,
        "currentpage": page,
        "limit": limit,
        "items": [dict(customer) for customer in customer_list]
    }

async def updateCustomer(customer_id: int, request: Request):
    validation_errors = []
    async with transaction_context() as transaction:
        try:
            # check xem là customer này có tồn tại hay không
            query = select(customer).where(customer.c.id == customer_id)
            existing_customer = await database.fetch_one(query)

            if not existing_customer:
                raise_custom_http_exception(404, "Customer not found")

            # Lấy dữ liệu input
            raw_data = await request.json()
            update_values = {}
            if "full_name" in raw_data:
                update_values['fullname'] = raw_data["full_name"]
            if "first_name" in raw_data:
                update_values['firstname'] = raw_data["first_name"]
            if "last_name" in raw_data:
                update_values['lastname'] = raw_data["last_name"]
            if "phone" in raw_data:
                if raw_data["phone"] != existing_customer["phone"]:
                    # Kiểm tra số điện thoại này đã tồn tại chưa
                    query = select(customer).where(customer.c.phone == raw_data["phone"])
                    customer_with_phone = await database.fetch_one(query)

                    if customer_with_phone:
                        raise_custom_http_exception(422, "Phone number already exists")
                update_values['phone'] = raw_data["phone"]
            if "note" in raw_data:
                update_values['note'] = raw_data["note"]
            if "gender" in raw_data:
                update_values['gender'] = raw_data["gender"]
            if "status" in raw_data:
                update_values['status'] = raw_data["status"]

            # Thêm cột updated_at
            update_values['updated_at'] = int(datetime.utcnow().timestamp())
            is_valid, validation_errors = validate_update_values(update_values)
            if not is_valid:
                raise_custom_http_exception(422, "Validation errors: " + ", ".join(validation_errors))

            # Cập nhật khách hàng
            query = (
                update(customer)
                .where(customer.c.id == customer_id)
                .values(**update_values)
            )
            await database.execute(query)

            # Trả về thông tin khách hàng đã cập nhật dưới dạng dictionary
            query = select(customer).where(customer.c.id == customer_id)
            updated_customer = await database.fetch_one(query)
            # return dict(updated_customer) if updated_customer else None
            return getJsonData(updated_customer)

        except Exception as e:
            if validation_errors :
                raise_custom_http_exception(422, "".join(validation_errors))
            else :
                raise_custom_http_exception(500, "Internal server error : " + str(e))
    

def create_error_response(status_code: int, message: str):
    return {"error": {"status_code": status_code, "message": message}}