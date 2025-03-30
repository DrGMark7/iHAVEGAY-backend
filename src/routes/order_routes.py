from fastapi import APIRouter, Depends, Path, Body, HTTPException, Query
from typing import List, Dict, Any, Optional
from src.controllers.order_controller import OrderController
from src.models.order_models import Order, ComputerSet, ShippingDetails
from src.database.database import Database
from src.utils.auth import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create-with-details", response_model=Order)
async def create_order_with_details(
    computer_set: ComputerSet = Body(..., description="Computer set details"),
    shipping_details: ShippingDetails = Body(..., description="Shipping details"),
    total_price: int = Body(..., ge=0, description="Total price"),
    current_user: Dict = Depends(get_current_user),
    order_controller: OrderController = Depends(lambda: OrderController(Database.get_instance()))
):
    """
    Create a new order with separate ComputerSet and ShippingDetails
    - **computer_set**: Computer set details
    - **shipping_details**: Shipping details
    - **total_price**: Total price
    """
    # Check if the user_id in shipping details matches the current user's ID
    if shipping_details.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Cannot create an order for another user")
    
    return await order_controller.create_order_with_details(
        user_id=current_user["user_id"],
        computer_set=computer_set,
        shipping_details=shipping_details,
        total_price=total_price
    )

@router.post("/", response_model=Order)
async def create_order(
    order_data: Dict[str, Any] = Body(...),
    current_user: Dict = Depends(get_current_user),
    order_controller: OrderController = Depends(lambda: OrderController(Database.get_instance()))
):
    """
    Create a new order
    - **user_id**: User ID
    - **order_details**: Computer set details
    - **shipping_details**: Shipping details
    - **total_price**: Total price
    """
    # Check if the user_id in the request matches the current user's ID
    if order_data.get("user_id") != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Cannot create an order for another user")
    
    return await order_controller.create_order(order_data)

@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: int = Path(..., description="Order ID to retrieve"),
    #! current_user: Dict = Depends(get_current_user),
    order_controller: OrderController = Depends(lambda: OrderController(Database.get_instance()))
):
    """
    Get order details by ID
    """
    order = await order_controller.get_order(order_id)
    
    #! Check if the user has permission to access this order
    #! if order.user_id != current_user["user_id"] and current_user["role"] != "admin":
    #!     raise HTTPException(status_code=403, detail="No permission to access this order")
    
    return order

@router.get("/", response_model=List[Order])
async def get_user_orders(
    user_id: Optional[int] = Query(None, description="Filter orders by user ID"),
    #! current_user: Dict = Depends(get_current_user),
    order_controller: OrderController = Depends(lambda: OrderController(Database.get_instance()))
):
    """
    Get all orders for a user
    """
    #! Check if the admin can see other users' orders
    #! if user_id and user_id != current_user["user_id"] and current_user["role"] != "admin":
    #!     raise HTTPException(status_code=403, detail="No permission to access other users' orders")
    
    #! If user_id is not specified, use the current user's ID
    #! query_user_id = user_id if user_id else current_user["user_id"]
    query_user_id = user_id
    
    return await order_controller.get_user_orders(query_user_id)

@router.patch("/{order_id}/status", response_model=Order)
async def update_order_status(
    order_id: int = Path(..., description="Order ID to update"),
    status: str = Body(..., embed=True),
    current_user: Dict = Depends(get_current_user),
    order_controller: OrderController = Depends(lambda: OrderController(Database.get_instance()))
):
    """
    Update order status
    - **status**: New status (Pending, Confirmed, Delivered, or Cancelled)
    """
    # Only admin users can update order status
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin users can update order status")
    
    return await order_controller.update_order_status(order_id, status)

@router.patch("/{order_id}/shipping", response_model=Order)
async def update_shipping_status(
    order_id: int = Path(..., description="Order ID to update"),
    shipping_status: str = Body(..., embed=True),
    current_user: Dict = Depends(get_current_user),
    order_controller: OrderController = Depends(lambda: OrderController(Database.get_instance()))
):
    """
    Update shipping status
    - **shipping_status**: New shipping status (Pending, Shipped, Delivered, or Cancelled)
    """
    # Only admin users can update shipping status
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin users can update shipping status")
    
    return await order_controller.update_shipping_status(order_id, shipping_status)

@router.delete("/{order_id}", response_model=Dict[str, bool])
async def delete_order(
    order_id: int = Path(..., description="Order ID to delete"),
    current_user: Dict = Depends(get_current_user),
    order_controller: OrderController = Depends(lambda: OrderController(Database.get_instance()))
):
    """
    Delete an order (admin only)
    """
    # Only admin users can delete orders
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin users can delete orders")
    
    success = await order_controller.delete_order(order_id)
    return {"success": success}
