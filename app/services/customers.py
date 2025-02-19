from urllib import request
from sqlalchemy import func, select, insert, update, delete
from app.database import database
from app.models.customers import customer
from app.schemas.customers import customerCreate, customerUpdate, customerInDB ,getJsonData
from app.models.logs import logs , log_action
from app.schemas.logs import ActionEnum, SourceTypeEnum
from datetime import datetime
from fastapi import HTTPException, Request
import time

async def addCustomers(customer_data: customerCreate, request: Request) -> customerInDB:
    query = select(customer).where(customer.c.phone == customer_data.phone)
    existing_customer = await database.fetch_one(query)
    
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer with this phone number already exists")

    timeday = time.time()
    query = insert(customer).values(
        fullname = customer_data.fullname,
        firstname = customer_data.firstname,
        lastname = customer_data.lastname,
        gender = customer_data.gender,
        phone = customer_data.phone,
        note = customer_data.note,
        created_at = int(timeday),
        updated_at = int(timeday),
        status = customer_data.status,
    )
    addCustomer = await database.execute(query)
    newCustomer = await getDetailCustomer(addCustomer)
    
    # Optional logging
    # await log_action(
    #     action=ActionEnum.CREATE,
    #     source_type=SourceTypeEnum.CUSTOMER,
    #     source_id=addCustomer,
    #     details=f"customer {customer_data.fullname} created",
    #     ip_address=request.client.host,
    #     user_agent = request.headers.get('User-Agent', 'unknown')
    # )
    
    return getJsonData(newCustomer)


async def getDetailCustomer(customer_id: int) -> customerInDB:
    query = select(customer).where(customer.c.id == customer_id)
    result = await database.fetch_one(query)
    if not result:
        error_response = create_error_response(404, "User not found")
        raise HTTPException(status_code=404, detail=error_response)
    return customerInDB(**result)

def create_error_response(status_code: int, message: str):
    return {"error": {"status_code": status_code, "message": message}}