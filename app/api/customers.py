from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Request
from app.schemas.customers import customerCreate, customerUpdate, customerInDB , customerResponse ,GenderEnum,StatusEnum, getJsonData
from app.services.customers import (
    addCustomers,
    listCustomers,
    updateCustomer
    # list_users_logic,
    # update_user_logic,
    # delete_user_logic
)

router = APIRouter()

@router.post("/", response_model=customerResponse, summary="Create a new customer", description="Create a new customer with the provided user details.")
async def addCustomer(request: Request):
    return await addCustomers(request)

@router.get("/", summary="Get a paginated list of customers with filters")
async def get_customers(
    fullname: Optional[str] = None, gender: Optional[GenderEnum] = None, 
    status: Optional[StatusEnum] = None,
    date_created_from: Optional[int] = None, date_created_to: Optional[int] = None, 
    customer_id: Optional[int] = None,
    page: int = 1, limit: int = 10
):
    return await listCustomers(
        fullname=fullname, gender=gender, status=status,
        date_created_from=date_created_from, date_created_to=date_created_to,
        customer_id=customer_id, page=page, limit=limit
    )

@router.put("/{customer_id}", response_model=customerResponse, summary="Update customer details", description="Update the details of an existing customer specified by ID.")
async def update_customer(customer_id: int, request: Request):
    updated_customer = await updateCustomer(customer_id, request)
    return updated_customer