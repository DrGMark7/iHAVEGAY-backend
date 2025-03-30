from fastapi import HTTPException
from src.database.database import Database
from src.models.order_models import ComputerSet, ShippingDetails, Order
from src.services.order_service import OrderService
from typing import List, Dict, Any

class OrderController:
    def __init__(self, database: Database):
        self.order_service = OrderService(database)
    
    async def create_order(self, order_data: Dict[str, Any]) -> Order:
        try:
            return await self.order_service.create_order(order_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def create_order_with_details(self, user_id: int, computer_set: ComputerSet, 
                                      shipping_details: ShippingDetails, total_price: int) -> Order:
        """
        Create a new order from separate ComputerSet and ShippingDetails
        """
        try:
            # Create order data in the format required by the service
            order_data = {
                "user_id": user_id,
                "order_details": computer_set.model_dump(),
                "shipping_details": shipping_details.model_dump(),
                "total_price": total_price
            }
            return await self.order_service.create_order(order_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def get_order(self, order_id: int) -> Order:
        try:
            return await self.order_service.get_order(order_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_user_orders(self, user_id: int) -> List[Order]:
        try:
            return await self.order_service.get_user_orders(user_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def update_order_status(self, order_id: int, status: str) -> Order:
        try:
            return await self.order_service.update_order_status(order_id, status)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def update_shipping_status(self, order_id: int, shipping_status: str) -> Order:
        try:
            return await self.order_service.update_shipping_status(order_id, shipping_status)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def delete_order(self, order_id: int) -> bool:
        try:
            return await self.order_service.delete_order(order_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

