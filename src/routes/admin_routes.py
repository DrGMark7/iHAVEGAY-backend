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

@router.get(
    "/products/top-selling",
    response_model=List[Dict[str, Any]],
    summary="Top selling products",
    description="Shows the top 5 best-selling products by quantity sold"
)
async def get_top_selling_products(limit: int = Query(5, ge=1, le=20)):
    """
    Retrieve the top selling products
    
    Parameters:
        limit (int): Number of items to display (default: 5, max: 20)
        
    Returns:
        List[Dict]: A list of top selling products:
        - product_id: Product identifier
        - title: Product name
        - category: Product category
        - sold_quantity: Number of units sold
        - price: Product price
    """
    try:
        return await controller.get_top_selling_products(limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving top selling products: {str(e)}"
        )

@router.get(
    "/products/compatible-mainboards/{cpu_id}",
    response_model=List[Dict[str, Any]],
    summary="Compatible mainboards for CPU",
    description="Shows mainboards compatible with the specified CPU based on socket"
)
async def get_compatible_mainboards(cpu_id: str):
    """
    Find mainboards compatible with the specified CPU
    
    Parameters:
        cpu_id (str): CPU identifier to find compatible mainboards for
        
    Returns:
        List[Dict]: A list of compatible mainboards:
        - mainboard_id: Mainboard identifier
        - title: Mainboard name
        - socket: Socket type
        - price: Price
        - quantity: Available stock
    """
    try:
        return await controller.get_compatible_mainboards(cpu_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving compatible mainboards: {str(e)}"
        )

@router.get(
    "/products/price-range",
    response_model=List[Dict[str, Any]],
    summary="Products by price range",
    description="Shows products within the specified price range and category"
)
async def get_products_by_price_range(
    category: str = Query(..., description="Product category (CPU, RAM, GPU, etc.)"),
    min_price: float = Query(0, description="Minimum price"),
    max_price: float = Query(1000000, description="Maximum price"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """
    Find products within a specified price range
    
    Parameters:
        category (str): Product category (CPU, RAM, GPU, etc.)
        min_price (float): Minimum price to search for
        max_price (float): Maximum price to search for
        limit (int): Maximum number of results (default: 10, max: 50)
        
    Returns:
        List[Dict]: A list of products within the specified price range:
        - product_id: Product identifier
        - title: Product name
        - price: Price
        - quantity: Available stock
    """
    try:
        return await controller.get_products_by_price_range(category, min_price, max_price, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving products by price range: {str(e)}"
        )

@router.get(
    "/analytics/frequently-bought-together",
    response_model=List[Dict[str, Any]],
    summary="Frequently bought together products",
    description="Shows pairs of products that are most frequently purchased together"
)
async def get_frequently_bought_together(limit: int = Query(5, ge=1, le=20)):
    """
    Find pairs of products that are frequently purchased together
    
    Parameters:
        limit (int): Number of product pairs to display (default: 5, max: 20)
        
    Returns:
        List[Dict]: A list of product pairs most frequently purchased together:
        - product_pair: The product pair
          - product1: First product information
          - product2: Second product information
        - frequency: Number of times purchased together
    """
    try:
        return await controller.get_frequently_bought_together(limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving frequently bought together products: {str(e)}"
        )

@router.get(
    "/products/recommended",
    response_model=List[Dict[str, Any]],
    summary="Recommended budget products",
    description="Shows the top 5 recommended products with the lowest prices"
)
async def get_recommended_products(
    category: str = Query(None, description="Product category (all categories if not specified)"),
    limit: int = Query(5, ge=1, le=20)
):
    """
    Retrieve recommended products with the lowest prices
    
    Parameters:
        category (str, optional): Product category to filter by (if not specified, will include all categories)
        limit (int): Number of items to display (default: 5, max: 20)
        
    Returns:
        List[Dict]: A list of recommended products with the lowest prices:
        - product_id: Product identifier
        - title: Product name
        - category: Product category
        - price: Price
        - quantity: Available stock
    """
    try:
        return await controller.get_recommended_products(category, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving recommended products: {str(e)}"
        )