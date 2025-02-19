from fastapi import APIRouter, HTTPException, Query, Request
from app.schemas.customers import customerCreate, customerUpdate, customerInDB , customerResponse , getJsonData
from app.services.customers import (
    addCustomers
    # get_user_logic,
    # list_users_logic,
    # update_user_logic,
    # delete_user_logic
)

router = APIRouter()

@router.post("/", response_model=customerResponse, summary="Create a new customer", description="Create a new customer with the provided user details.")
async def addCustomer(user: customerCreate, request: Request):
    return await addCustomers(user, request)
