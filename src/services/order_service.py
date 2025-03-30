from fastapi import HTTPException
from datetime import datetime, timezone
from src.database.database import Database
from src.models.order_models import Order, ComputerSet, ShippingDetails

class OrderService:
    def __init__(self, database: Database):
        self.db = database
        self.collection = "orders"

    async def create_order(self, order_data: dict) -> Order:
        # Generate order ID (in a real application, this should be more sophisticated)
        # Get the collection first
        collection = await self.db.get_collection(self.collection)
        
        # Find latest order
        latest_order = await collection.find_one(sort=[("order_id", -1)])
        new_order_id = 10000 if not latest_order else latest_order["order_id"] + 1
        
        # Create order with current timestamp
        order_data["order_id"] = new_order_id
        order_data["order_date"] = datetime.now(timezone.utc)
        order_data["status"] = "Pending"  # Default status for new orders
        
        # Ensure shipping details have the same order_id
        if "shipping_details" in order_data and isinstance(order_data["shipping_details"], dict):
            order_data["shipping_details"]["order_id"] = new_order_id
        
        # Check if order_details exists in ComputerSet format
        if "order_details" not in order_data and isinstance(order_data.get("computer_set"), dict):
            order_data["order_details"] = order_data.pop("computer_set")
        
        # Create order object for validation
        try:
            order = Order(**order_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid order data: {str(e)}")
        
        # Insert into database
        result = await collection.insert_one(order.model_dump())
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create order")
        
        return order

    async def get_order(self, order_id: int) -> Order:
        collection = await self.db.get_collection(self.collection)
        order_data = await collection.find_one({"order_id": order_id})
        if not order_data:
            raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
        
        return Order(**order_data)

    async def get_user_orders(self, user_id: int) -> list[Order]:
        collection = await self.db.get_collection(self.collection)
        cursor = collection.find({"user_id": user_id})
        orders_data = await cursor.to_list(length=100)  # Limit to 100 orders
        
        if not orders_data:
            return []
        
        return [Order(**order) for order in orders_data]

    async def update_order_status(self, order_id: int, status: str) -> Order:
        # Validate status
        valid_statuses = ["Pending", "Confirmed", "Delivered", "Cancelled"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
        
        # Get collection
        collection = await self.db.get_collection(self.collection)
        
        # Update order
        update_result = await collection.update_one(
            {"order_id": order_id}, 
            {"$set": {"status": status}}
        )
        
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
        
        # Get updated order
        return await self.get_order(order_id)

    async def update_shipping_status(self, order_id: int, shipping_status: str) -> Order:
        # Validate status
        valid_statuses = ["Pending", "Shipped", "Delivered", "Cancelled"]
        if shipping_status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid shipping status. Must be one of {valid_statuses}")
        
        # Get collection
        collection = await self.db.get_collection(self.collection)
        
        # Update shipping status
        update_result = await collection.update_one(
            {"order_id": order_id}, 
            {"$set": {"shipping_details.shipping_status": shipping_status}}
        )
        
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
        
        # Get updated order
        return await self.get_order(order_id)

    async def delete_order(self, order_id: int) -> bool:
        collection = await self.db.get_collection(self.collection)
        delete_result = await collection.delete_one({"order_id": order_id})
        
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
        
        return True
