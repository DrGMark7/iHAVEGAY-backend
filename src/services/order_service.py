from fastapi import HTTPException
from datetime import datetime, timezone
from src.database.database import Database
from src.models.order_models import Order, ComputerSet, ShippingDetails
import asyncio

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
        
        # Check and update inventory quantities
        if "order_details" in order_data or "computer_set" in order_data:
            computer_set = order_data.get("order_details") or order_data.get("computer_set")
            await self.check_and_update_inventory(computer_set)
        
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

    async def check_and_update_inventory(self, computer_set: dict) -> None:
        """
        Check if all items in the computer set are available in sufficient quantity
        and update the inventory by reducing the quantity for each item.
        """
        inventory_updates = []
        
        # Check CPU if present
        if cpu_id := computer_set.get("cpu_id"):
            inventory_updates.append(self.check_and_prepare_update("CPUs", {"cpu_id": cpu_id}))
            
        # Check RAM if present
        if ram_id := computer_set.get("ram_id"):
            inventory_updates.append(self.check_and_prepare_update("Rams", {"ram_id": ram_id}))
            
        # Check Mainboard if present
        if mb_id := computer_set.get("mainboard_id"):
            inventory_updates.append(self.check_and_prepare_update("Mainboards", {"mainboard_id": mb_id}))
            
        # Check SSD if present
        if ssd_id := computer_set.get("ssd_id"):
            inventory_updates.append(self.check_and_prepare_update("SSDs", {"ssd_id": ssd_id}))
            
        # Check M2 if present
        if m2_id := computer_set.get("m2_id"):
            inventory_updates.append(self.check_and_prepare_update("M2s", {"m2_id": m2_id}))
            
        # Check GPU if present
        if gpu_id := computer_set.get("gpu_id"):
            inventory_updates.append(self.check_and_prepare_update("GPUs", {"gpu_id": gpu_id}))
            
        # Check Case if present
        if case_id := computer_set.get("case_id"):
            inventory_updates.append(self.check_and_prepare_update("Cases", {"case_id": case_id}))
            
        # Check PSU if present
        if psu_id := computer_set.get("psu_id"):
            inventory_updates.append(self.check_and_prepare_update("PSUs", {"psu_id": psu_id}))
        
        # Execute all inventory checks and updates
        results = await asyncio.gather(*inventory_updates, return_exceptions=True)
        
        # Check if any errors occurred
        errors = [result for result in results if isinstance(result, Exception)]
        if errors:
            error_messages = [str(err) for err in errors]
            raise HTTPException(status_code=400, detail=f"Inventory issues: {', '.join(error_messages)}")
    
    async def check_and_prepare_update(self, collection_name: str, query: dict) -> None:
        """
        Check if an item exists in the collection and has sufficient quantity.
        If yes, update the inventory by reducing the quantity by 1.
        """
        collection = await self.db.get_collection(collection_name)
        
        # Check if the item exists and has sufficient quantity
        item = await collection.find_one(query)
        if not item:
            id_field = list(query.keys())[0]
            id_value = query[id_field]
            raise HTTPException(status_code=404, detail=f"Item with {id_field}={id_value} not found")
        
        if item["quantity"] < 1:
            id_field = list(query.keys())[0]
            id_value = query[id_field]
            raise HTTPException(status_code=400, detail=f"Item with {id_field}={id_value} is out of stock")
        
        # Update the inventory by reducing the quantity by 1
        result = await collection.update_one(
            query,
            {"$inc": {"quantity": -1}}
        )
        
        if result.modified_count == 0:
            id_field = list(query.keys())[0]
            id_value = query[id_field]
            raise HTTPException(status_code=500, detail=f"Failed to update inventory for {id_field}={id_value}")

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
        
        # Get the current order to check if status is changing to/from Cancelled
        current_order = await self.get_order(order_id)
        
        # If order is being cancelled, restore inventory quantities
        if status == "Cancelled" and current_order.status != "Cancelled":
            if hasattr(current_order, "order_details") and current_order.order_details:
                await self.restore_inventory(current_order.order_details.model_dump())
        
        # If order is being un-cancelled, deduct inventory quantities again
        if current_order.status == "Cancelled" and status != "Cancelled":
            if hasattr(current_order, "order_details") and current_order.order_details:
                await self.check_and_update_inventory(current_order.order_details.model_dump())
        
        # Update order
        update_result = await collection.update_one(
            {"order_id": order_id}, 
            {"$set": {"status": status}}
        )
        
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
        
        # Get updated order
        return await self.get_order(order_id)

    async def restore_inventory(self, computer_set: dict) -> None:
        """
        Restore inventory quantities when an order is cancelled.
        """
        inventory_updates = []
        
        # Restore CPU if present
        if cpu_id := computer_set.get("cpu_id"):
            inventory_updates.append(self.restore_item_quantity("cpus", {"cpu_id": cpu_id}))
            
        # Restore RAM if present
        if ram_id := computer_set.get("ram_id"):
            inventory_updates.append(self.restore_item_quantity("rams", {"ram_id": ram_id}))
            
        # Restore Mainboard if present
        if mb_id := computer_set.get("mainboard_id"):
            inventory_updates.append(self.restore_item_quantity("mainboards", {"mainboard_id": mb_id}))
            
        # Restore SSD if present
        if ssd_id := computer_set.get("ssd_id"):
            inventory_updates.append(self.restore_item_quantity("ssds", {"ssd_id": ssd_id}))
            
        # Restore M2 if present
        if m2_id := computer_set.get("m2_id"):
            inventory_updates.append(self.restore_item_quantity("m2s", {"m2_id": m2_id}))
            
        # Restore GPU if present
        if gpu_id := computer_set.get("gpu_id"):
            inventory_updates.append(self.restore_item_quantity("gpus", {"gpu_id": gpu_id}))
            
        # Restore Case if present
        if case_id := computer_set.get("case_id"):
            inventory_updates.append(self.restore_item_quantity("cases", {"case_id": case_id}))
            
        # Restore PSU if present
        if psu_id := computer_set.get("psu_id"):
            inventory_updates.append(self.restore_item_quantity("psus", {"psu_id": psu_id}))
        
        # Execute all inventory restorations
        await asyncio.gather(*inventory_updates, return_exceptions=True)
    
    async def restore_item_quantity(self, collection_name: str, query: dict) -> None:
        """
        Increase the quantity of an item by 1 when an order is cancelled.
        """
        collection = await self.db.get_collection(collection_name)
        
        # Update the inventory by increasing the quantity by 1
        await collection.update_one(
            query,
            {"$inc": {"quantity": 1}}
        )

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
        # Get the order first to restore inventory if necessary
        try:
            order = await self.get_order(order_id)
            
            # Restore inventory quantities if order is not cancelled
            if order.status != "Cancelled" and hasattr(order, "order_details") and order.order_details:
                await self.restore_inventory(order.order_details.model_dump())
                
            # Delete the order
            collection = await self.db.get_collection(self.collection)
            delete_result = await collection.delete_one({"order_id": order_id})
            
            if delete_result.deleted_count == 0:
                raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
            
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete order: {str(e)}")
