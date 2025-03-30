from fastapi import APIRouter, HTTPException, status, Query
from src.controllers.admin_controller import AdminController
from typing import List, Dict, Any

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Data not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Requested data not found"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        }
    }
)

controller = AdminController()

@router.get(
    "/sales/last-five-days",
    response_model=List[Dict[str, Any]],
    summary="Sales for the last 5 days",
    description="Summary of sales for the last 5 days showing daily sales totals"
)
async def get_sales_last_five_days():
    """
    Retrieve sales data for the last 5 days
    
    Returns:
        List[Dict]: A list of daily sales data for the last 5 days:
        - date: Date (YYYY-MM-DD)
        - total_sales: Total sales amount for the day
        - order_count: Number of orders for the day
    """
    try:
        return await controller.get_sales_last_five_days()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving sales data: {str(e)}"
        )

@router.get(
    "/inventory/low-stock",
    response_model=List[Dict[str, Any]],
    summary="Products with lowest stock",
    description="Shows the top 5 products with the lowest stock quantity"
)
async def get_low_stock_products(limit: int = Query(5, ge=1, le=20)):
    """
    Retrieve products with the lowest stock quantity
    
    Parameters:
        limit (int): Number of items to display (default: 5, max: 20)
        
    Returns:
        List[Dict]: A list of products with the lowest stock:
        - product_id: Product identifier
        - title: Product name
        - stock_quantity: Available quantity
        - price: Product price
        - category: Product category
    """
    try:
        return await controller.get_low_stock_products(limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving low stock products: {str(e)}"
        )

@router.get(
    "/orders/recent",
    response_model=List[Dict[str, Any]],
    summary="Recent orders",
    description="Shows the 5 most recent orders"
)
async def get_recent_orders(limit: int = Query(5, ge=1, le=20)):
    """
    Retrieve the most recent orders
    
    Parameters:
        limit (int): Number of items to display (default: 5, max: 20)
        
    Returns:
        List[Dict]: A list of the most recent orders sorted by date:
        - order_id: Order identifier
        - customer_id: Customer identifier
        - order_date: Order date
        - total_amount: Order total
        - status: Order status
    """
    try:
        return await controller.get_recent_orders(limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving recent orders: {str(e)}"
        )

@router.get(
    "/inventory/summary",
    response_model=Dict[str, Any],
    summary="Inventory summary",
    description="Summary of inventory quantities by category"
)
async def get_inventory_summary():
    """
    Retrieve a summary of inventory in the system
    
    Returns:
        Dict: Inventory summary data:
        - categories: Summary by category
          - category: Category name
          - total_items: Number of product items
          - total_stock: Total stock quantity
          - total_value: Total value
        - total: Overall summary
          - total_items: Total number of product items
          - total_stock: Total stock quantity
          - total_value: Total value
    """
    try:
        return await controller.get_inventory_summary()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving inventory summary: {str(e)}"
        )

@router.get(
    "/customers/top",
    response_model=List[Dict[str, Any]],
    summary="Top customers",
    description="Shows the top 5 customers by order count"
)
async def get_top_customers(limit: int = Query(5, ge=1, le=20)):
    """
    Retrieve the top customers by order count
    
    Parameters:
        limit (int): Number of items to display (default: 5, max: 20)
        
    Returns:
        List[Dict]: A list of top customers by order count:
        - customer_id: Customer identifier
        - name: Customer name
        - email: Customer email
        - order_count: Total number of orders
        - total_spent: Total amount spent
    """
    try:
        return await controller.get_top_customers(limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving top customers: {str(e)}"
        )