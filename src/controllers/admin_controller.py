from fastapi import HTTPException
from datetime import datetime, timedelta
from src.database.database import Database
from typing import List, Dict, Any

class AdminController:
    def __init__(self):
        self.orders_collection = None
        self.users_collection = None
        self.hardware_collections = {}
        self._init_collections()

    async def _init_collections(self):
        """Initialize MongoDB collections asynchronously"""
        self.orders_collection = await Database.get_collection('orders')
        self.users_collection = await Database.get_collection('users')
        
        # Initialize hardware collections
        hardware_types = [
            "CPUs", "RAMs", "Mainboards", "GPUs", "Cases", "PSUs", "SSDs", "M2s"
        ]
        for hw_type in hardware_types:
            self.hardware_collections[hw_type] = await Database.get_collection(hw_type)

    async def get_sales_last_five_days(self):
        """
        Get sales data for the last 5 days
        """
        if self.orders_collection is None:
            await self._init_collections()
        
        today = datetime.now()
        results = []
        
        for i in range(5):
            target_date = today - timedelta(days=i)
            start_of_day = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0)
            end_of_day = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59)
            
            pipeline = [
                {
                    "$match": {
                        "order_date": {
                            "$gte": start_of_day,
                            "$lte": end_of_day
                        }
                        # "status": {"$in": ["Confirmed", "Delivered"]}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total_sales": {"$sum": "$total_price"},
                        "order_count": {"$sum": 1}
                    }
                }
            ]
            
            cursor = self.orders_collection.aggregate(pipeline)
            sales_data = await cursor.to_list(length=1)
            
            date_str = target_date.strftime("%Y-%m-%d")
            if sales_data and len(sales_data) > 0:
                results.append({
                    "date": date_str,
                    "total_sales": sales_data[0].get("total_sales", 0),
                    "order_count": sales_data[0].get("order_count", 0)
                })
            else:
                results.append({
                    "date": date_str,
                    "total_sales": 0,
                    "order_count": 0
                })
        
        return results

    async def get_low_stock_products(self, limit: int = 5):
        """
        Get top 5 products with the lowest stock quantity
        """
        # Make sure collections are initialized
        if self.orders_collection is None:
            await self._init_collections()
        
        # Define hardware collections mapping
        hardware_mapping = [
            {"collection_name": "CPUs", "category": "CPU", "id_field": "cpu_id"},
            {"collection_name": "RAMs", "category": "RAM", "id_field": "ram_id"},
            {"collection_name": "Mainboards", "category": "Mainboard", "id_field": "mainboard_id"},
            {"collection_name": "GPUs", "category": "GPU", "id_field": "gpu_id"},
            {"collection_name": "Cases", "category": "Case", "id_field": "case_id"},
            {"collection_name": "PSUs", "category": "PSU", "id_field": "psu_id"},
            {"collection_name": "SSDs", "category": "SSD", "id_field": "ssd_id"},
            {"collection_name": "M2s", "category": "M2", "id_field": "m2_id"}
        ]
        
        # List to store products from all collections
        all_low_stock = []
        
        # Fetch low stock products from each collection
        for hw in hardware_mapping:
            try:
                # Get the collection directly each time instead of storing in a dict
                collection = await Database.get_collection(hw["collection_name"])
                
                category = hw["category"]
                id_field = hw["id_field"]
                
                pipeline = [
                    {
                        "$match": {
                            "quantity": {"$gt": 0}
                        }
                    },
                    {
                        "$sort": {"quantity": 1}
                    },
                    {
                        "$limit": limit
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "product_id": f"${id_field}",
                            "title": 1,
                            "stock_quantity": "$quantity",
                            "price": 1,
                            "category": {"$literal": category}
                        }
                    }
                ]
                
                cursor = collection.aggregate(pipeline)
                result = await cursor.to_list(length=limit)
                all_low_stock.extend(result)
            except Exception as e:
                print(f"Error fetching low stock products for {hw['category']}: {e}")
                # Continue to next collection if there's an error
                continue
        
        # Sort combined results by stock quantity
        all_low_stock.sort(key=lambda x: x.get("stock_quantity", 999999))
        
        # Return only the top N results
        return all_low_stock[:limit]

    async def get_recent_orders(self, limit: int = 5):
        """
        Get the 5 most recent orders
        """
        if self.orders_collection is None:
            await self._init_collections()
        
        # Check if collection exists and has data
        count = await self.orders_collection.count_documents({})
        if count == 0:
            return []
        
        # Get recent orders with important order fields
        cursor = self.orders_collection.find(
            {},  # Get all orders regardless of status
            {
                "_id": 0,
                "order_id": 1,
                "user_id": 1,
                "order_date": 1,
                "total_price": 1,
                "status": 1,
                "order_details": 1,  # Include order_details
                "shipping_details.shipping_status": 1  # Include shipping status
            }
        ).sort("order_date", -1).limit(limit)
        
        orders = await cursor.to_list(length=limit)
        
        # Enhance orders with user info
        enhanced_orders = []
        for order in orders:
            # Get basic user info
            if "user_id" in order:
                user = await self.users_collection.find_one(
                    {"user_id": order["user_id"]},
                    {"_id": 0, "username": 1, "email": 1}
                )
                if user:
                    order["user_info"] = user
            
            enhanced_orders.append(order)
            
        return enhanced_orders

    async def get_inventory_summary(self):
        """
        Get inventory summary by category
        """
        # Make sure collections are initialized
        if self.orders_collection is None:
            await self._init_collections()
            
        hardware_types = [
            {"name": "CPUs", "category": "CPU"},
            {"name": "Rams", "category": "RAM"},
            {"name": "Mainboards", "category": "Mainboard"},
            {"name": "GPUs", "category": "GPU"},
            {"name": "Cases", "category": "Case"},
            {"name": "PSUs", "category": "PSU"},
            {"name": "SSDs", "category": "SSD"},
            {"name": "M2s", "category": "M2"}
        ]
        
        category_summary = []
        total_items = 0
        total_stock = 0
        total_value = 0
        
        for hw in hardware_types:
            try:
                # Get the collection directly each time
                collection = await Database.get_collection(hw["name"])
                
                # Get summary for this category
                pipeline = [
                    {
                        "$group": {
                            "_id": None,
                            "total_items": {"$sum": 1},
                            "total_stock": {"$sum": "$quantity"},
                            "total_value": {"$sum": {"$multiply": ["$price", "$quantity"]}}
                        }
                    }
                ]
                
                cursor = collection.aggregate(pipeline)
                result = await cursor.to_list(length=1)
                
                if result and len(result) > 0:
                    category_data = {
                        "category": hw["category"],
                        "total_items": result[0].get("total_items", 0),
                        "total_stock": result[0].get("total_stock", 0),
                        "total_value": result[0].get("total_value", 0)
                    }
                    category_summary.append(category_data)
                    
                    # Add to totals
                    total_items += category_data["total_items"]
                    total_stock += category_data["total_stock"]
                    total_value += category_data["total_value"]
                else:
                    category_summary.append({
                        "category": hw["category"],
                        "total_items": 0,
                        "total_stock": 0,
                        "total_value": 0
                    })
            except Exception as e:
                print(f"Error getting inventory summary for {hw['category']}: {e}")
                category_summary.append({
                    "category": hw["category"],
                    "total_items": 0,
                    "total_stock": 0,
                    "total_value": 0
                })
        
        return {
            "categories": category_summary,
            "total": {
                "total_items": total_items,
                "total_stock": total_stock,
                "total_value": total_value
            }
        }

    async def get_top_customers(self, limit: int = 5):  
        """
        Top 5 customers by total order count
        """
        if self.orders_collection is None or self.users_collection is None:
            await self._init_collections()
        
        pipeline = [
            {
                "$group": {
                    "_id": "$user_id",
                    "order_count": {"$sum": 1},
                    "total_spent": {"$sum": "$total_price"}
                }
            },
            {
                "$sort": {"total_spent": -1}
            },
            {
                "$limit": limit
            },
            {
                "$lookup": {
                    "from": "users",  # lowercase collection name
                    "localField": "_id",
                    "foreignField": "user_id",
                    "as": "user_info"
                }
            },
            {
                "$unwind": {
                    "path": "$user_info",
                    "preserveNullAndEmptyArrays": True  # Keep results even if no user found
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "user_id": "$_id",
                    "username": "$user_info.username",
                    "email": "$user_info.email",
                    "order_count": 1,
                    "total_spent": 1
                }
            }
        ]
        
        try:
            cursor = self.orders_collection.aggregate(pipeline)
            return await cursor.to_list(length=limit)
        except Exception as e:
            print(f"Error getting top customers: {e}")
            return []
