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
            "CPUs", "Rams", "Mainboards", "GPUs", "Cases", "PSUs", "SSDs", "M2s"
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
            {"collection_name": "Rams", "category": "RAM", "id_field": "ram_id"},
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
                
                # Find products with low stock
                cursor = collection.find(
                    {"quantity": {"$lt": 5}},
                    {"_id": 0}  # Exclude only _id, include all other fields
                ).sort("quantity", 1)
                
                results = await cursor.to_list()
                
                # Add category field for standardization
                for product in results:
                    product["category"] = category
                
                all_low_stock.extend(results)
            except Exception as e:
                print(f"Error fetching low stock products for {hw['category']}: {e}")
                # Continue to next collection if there's an error
                continue
        
        # Sort combined results by stock quantity
        all_low_stock.sort(key=lambda x: x.get("quantity", 999999))
        
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

    async def get_top_selling_products(self, limit: int = 5):
        """
        Get the top 5 best-selling products
        """
        if self.orders_collection is None:
            await self._init_collections()
        
        # First check if there are orders with order_details as object
        count = await self.orders_collection.count_documents({
            "order_details": { "$exists": True }
        })
        
        if count == 0:
            print("No orders with order_details found")
            return []
        
        # Check data structure of order_details in the first document
        sample = await self.orders_collection.find_one({"order_details": {"$exists": True}})
        is_array = isinstance(sample.get("order_details"), list) if sample else False
        
        # Handle based on structure
        if is_array:
            # Original pipeline for array structure
            pipeline = [
                # Filter orders that have order_details as an array
                {
                    "$match": {
                        "order_details": { "$exists": True, "$type": "array" }
                    }
                },
                # Unwind order details to process each product separately
                { "$unwind": "$order_details" },
                # Group by product and sum quantities
                { 
                    "$group": {
                        "_id": {
                            "product_id": "$order_details.product_id",
                            "category": { "$ifNull": ["$order_details.category", "Unknown"] }
                        },
                        "sold_quantity": { "$sum": { "$ifNull": ["$order_details.quantity", 1] } },
                        "product_title": { "$first": { "$ifNull": ["$order_details.title", "Unknown Product"] } },
                        "price": { "$first": { "$ifNull": ["$order_details.price", 0] } }
                    }
                }
            ]
        else:
            # Pipeline for object structure (where order_details is an object with product IDs)
            # First get all hardware types in the order_details
            hw_types = [
                {"field": "cpu_id", "category": "CPU"},
                {"field": "ram_id", "category": "Ram"},
                {"field": "mainboard_id", "category": "Mainboard"},
                {"field": "gpu_id", "category": "GPU"},
                {"field": "case_id", "category": "Case"},
                {"field": "psu_id", "category": "PSU"},
                {"field": "ssd_id", "category": "SSD"},
                {"field": "m2_id", "category": "M2"}
            ]
            
            # Create a separate pipeline for each hardware type
            all_results = []
            for hw in hw_types:
                field = hw["field"]
                category = hw["category"]
                
                # Pipeline for this hardware type
                type_pipeline = [
                    # Match orders that have this hardware type in order_details
                    {
                        "$match": {
                            f"order_details.{field}": { "$exists": True }
                        }
                    },
                    # Group by hardware ID and count occurrences
                    {
                        "$group": {
                            "_id": f"$order_details.{field}",
                            "sold_quantity": { "$sum": 1 },
                            "count": { "$sum": 1 },
                            "product_title": { "$first": "$order_details.title" }
                        }
                    },
                    # Add category information
                    {
                        "$project": {
                            "_id": 0,
                            "product_id": "$_id",
                            "category": { "$literal": category },
                            "sold_quantity": 1,
                        }
                    }
                ]
                
                try:
                    cursor = self.orders_collection.aggregate(type_pipeline)
                    results = await cursor.to_list(length=100)
                    
                    # For each result, try to get title and price from the corresponding collection
                    if results:
                        collection_name = f"{category}s"
                        if collection_name in self.hardware_collections:
                            collection = self.hardware_collections[collection_name]
                            if collection is not None:
                                for item in results:
                                    id_field = field
                                    product = await collection.find_one({id_field: item["product_id"]})
                                    #! Debug RAM 20001
                                    # if category == "RAM" and item["product_id"] == 20001:
                                    #     print(product)
                                    if product:
                                        item["title"] = product.get("title", "Unknown")
                                        item["price"] = product.get("price", 0)
                                        item["imgUrl"] = product.get("imgUrl", "")
                                        item["brand"] = product.get("brand", "")
                                        item["quantity"] = product.get("quantity", 0)
                                    else:
                                        item["title"] = f"Unknown {category}"
                                        item["price"] = 0
                                        item["imgUrl"] = product.get("imgUrl", "")
                                        item["brand"] = product.get("brand", "")
                                        item["quantity"] = product.get("quantity", 0)
                        
                    all_results.extend(results)
                except Exception as e:
                    print(f"Error processing {category}: {e}")
                    continue
            
            # Sort the combined results by sold quantity
            all_results.sort(key=lambda x: x.get("sold_quantity", 0), reverse=True)
            
            # Take only the top N results
            return all_results[:limit] if all_results else []
            
        # Continue with common pipeline steps for array structure
        if is_array:
            pipeline.extend([
                # Sort by sold quantity in descending order
                { "$sort": { "sold_quantity": -1 } },
                # Limit to requested number of results
                { "$limit": limit },
                # Format the final output
                {
                    "$project": {
                        "_id": 0,
                        "product_id": "$_id.product_id",
                        "category": "$_id.category",
                        "title": "$product_title",
                        "sold_quantity": 1,
                        "price": 1,
                        "imgUrl": 1
                    }
                }
            ])
            
            try:
                cursor = self.orders_collection.aggregate(pipeline)
                results = await cursor.to_list(length=limit)
                if results:
                    return results
            except Exception as e:
                print(f"Error getting top selling products: {e}")
        
        # Return empty list instead of sample data
        print("No top selling products found, returning empty list")
        return []

    async def get_compatible_mainboards(self, cpu_id: str):
        """
        Find mainboards compatible with the specified CPU based on socket
        """
        if not self.hardware_collections:
            await self._init_collections()
        
        # Check if required collections exist in hardware_collections
        if "CPUs" not in self.hardware_collections or "Mainboards" not in self.hardware_collections:
            raise HTTPException(status_code=404, detail="Required hardware collections not found")
        
        # Get CPU collection and mainboard collection
        cpu_collection = self.hardware_collections.get("CPUs")
        mainboard_collection = self.hardware_collections.get("Mainboards")
        
        # Check if collections are None
        if cpu_collection is None or mainboard_collection is None:
            raise HTTPException(status_code=404, detail="Required hardware collections are None")
        
        # Find the CPU by ID
        cpu = await cpu_collection.find_one({"cpu_id": int(cpu_id)})
        if not cpu:
            raise HTTPException(status_code=404, detail=f"CPU with ID {cpu_id} not found")
        
        socket = cpu.get("Socket")
        if not socket:
            raise HTTPException(status_code=400, detail="CPU socket information is missing")
        
        try:
            # Find mainboards with matching socket, excluding only _id
            cursor = mainboard_collection.find(
                {"socket": socket},
                {"_id": 0}  # Exclude only _id, include all other fields
            )
            
            # Get results
            results = await cursor.to_list(length=100)
            
            # If no compatible mainboards found, return empty list
            if not results:
                print(f"No compatible mainboards found for socket {socket}")
                return []
                
            return results
            
        except Exception as e:
            print(f"Error finding compatible mainboards: {e}")
            return []

    async def get_products_by_price_range(self, category: str, min_price: float, max_price: float, limit: int = 10):
        """
        Find products within a specified price range
        """
        if not self.hardware_collections:
            await self._init_collections()
        
        # Map category names to collection names
        category_mapping = {
            "CPU": "CPUs",
            "RAM": "Rams",
            "MAINBOARD": "Mainboards",
            "GPU": "GPUs",
            "CASE": "Cases",
            "PSU": "PSUs",
            "SSD": "SSDs",
            "M2": "M2s"
        }
        
        collection_name = category_mapping.get(category)
        if not collection_name:
            raise HTTPException(status_code=400, detail=f"Invalid product category: '{category}'")
        
        collection = await Database.get_collection(collection_name)
        
        # Determine the ID field based on the category
        id_field = f"{category.lower()}_id"
        if category == "M2":
            id_field = "m2_id"
        
        # Find products within the price range
        query = {
            "price": {
                "$gte": min_price,
                "$lte": max_price
            }
        }
        
        # Only exclude _id, include all other fields
        cursor = collection.find(query, {"_id": 0}).sort("price", 1).limit(limit)
        results = await cursor.to_list(length=limit)
        
        # Add standard category field
        for item in results:
            item["category"] = category
        
        return results

    async def get_frequently_bought_together(self, limit: int = 5):
        """
        Find pairs of products that are frequently purchased together
        """
        if self.orders_collection is None:
            await self._init_collections()
        
        # Define hardware types
        hw_types = [
            {"field": "cpu_id", "category": "CPU", "collection": "CPUs"},
            {"field": "ram_id", "category": "RAM", "collection": "Rams"},
            {"field": "mainboard_id", "category": "MAINBOARDS", "collection": "Mainboards"},
            {"field": "gpu_id", "category": "GPU", "collection": "GPUs"},
            {"field": "case_id", "category": "CASES", "collection": "Cases"},
            {"field": "psu_id", "category": "PSU", "collection": "PSUs"},
            {"field": "ssd_id", "category": "SSD", "collection": "SSDs"},
            {"field": "m2_id", "category": "M2", "collection": "M2s"}
        ]
        
        # First, check if we have orders with order_details as object
        count = await self.orders_collection.count_documents({
            "order_details": { "$exists": True }
        })
        
        if count == 0:
            print("No orders with order_details found")
            return []
        
        # Check data structure of order_details in the first document
        sample = await self.orders_collection.find_one({"order_details": {"$exists": True}})
        is_array = isinstance(sample.get("order_details"), list) if sample else False
        
        # If order_details is an array, use the existing implementation
        if is_array:
            print("Using array implementation for order_details")
            return await self._get_frequently_bought_together_array(limit)
        
        # Otherwise, create a custom implementation for object structure
        print("Using object implementation for order_details")
        
        # First, get a list of all orders that have order_details as an object
        orders = await self.orders_collection.find(
            {"order_details": {"$exists": True, "$type": "object"}},
            {"_id": 0, "order_id": 1, "order_details": 1}
        ).to_list(length=100)
        
        if not orders:
            return []
        
        # Count frequencies of product pairs
        product_pairs = {}
        product_info = {}
        
        # Retrieve product info for all hardware types
        for hw in hw_types:
            try:
                # Get a reference to the collection for this hardware type
                collection_name = hw["collection"]
                if collection_name not in self.hardware_collections:
                    print(f"Collection {collection_name} not found in hardware_collections")
                    continue
                
                collection = self.hardware_collections[collection_name]
                if collection is None:
                    print(f"Collection {collection_name} is None")
                    continue
                
                # Get the field name that contains the product ID
                id_field = hw["field"]
                
                # Find all products of this type
                products_cursor = collection.find(
                    {}, 
                    # {"_id": 0, id_field: 1, "title": 1}
                )
                
                products = await products_cursor.to_list(length=100)
                
                # Store product info for later use
                for product in products:
                    product_id = product.get(id_field)
                    if product_id:
                        product_info[f"{id_field}:{product_id}"] = {
                            "product_id": product_id,
                            "title": product.get("title", f"Unknown {hw['category']}"),
                            "category": hw["category"],
                            "imgUrl": product.get("imgUrl", ""),
                            "brand": product.get("brand", ""),
                            "quantity": product.get("quantity", 0),
                            "price": product.get("price", 0)
                        }
                        

            except Exception as e:
                print(f"Error retrieving products for {hw['category']}: {e}")
                continue
        
        # Process each order to find product pairs
        for order in orders:
            order_details = order.get("order_details", {})
            
            # Build a list of products in this order
            products_in_order = []
            for hw in hw_types:
                product_id = order_details.get(hw["field"])
                if product_id:
                    products_in_order.append({
                        "hw_field": hw["field"],
                        "product_id": product_id,
                        "category": hw["category"]
                    })
            
            # Create pairs from products in the order
            for i in range(len(products_in_order)):
                for j in range(i + 1, len(products_in_order)):
                    # Create a sorted pair key to avoid counting A-B and B-A separately
                    product1 = products_in_order[i]
                    product2 = products_in_order[j]
                    
                    # Sort by hw_field to ensure consistent pairing
                    if product1["hw_field"] > product2["hw_field"]:
                        product1, product2 = product2, product1
                    
                    pair_key = f"{product1['hw_field']}:{product1['product_id']}_{product2['hw_field']}:{product2['product_id']}"
                    
                    # Increment the pair count
                    if pair_key in product_pairs:
                        product_pairs[pair_key]["frequency"] += 1
                    else:
                        product_pairs[pair_key] = {
                            "product_pair": {
                                "product1": product_info.get(f"{product1['hw_field']}:{product1['product_id']}", {
                                    "product_id": product1["product_id"],
                                    "title": f"Unknown {product1['category']}",
                                    "category": product1["category"]
                                }),
                                "product2": product_info.get(f"{product2['hw_field']}:{product2['product_id']}", {
                                    "product_id": product2["product_id"],
                                    "title": f"Unknown {product2['category']}",
                                    "category": product2["category"]
                                })
                            },
                            "frequency": 1
                        }
        
        # Convert to list and sort by frequency
        result = list(product_pairs.values())
        result.sort(key=lambda x: x["frequency"], reverse=True)
        
        # If no real data was processed, return empty list
        if not result:
            print("No product pairs found, returning empty list")
            return []
        
        # Take only the top N results
        return result[:limit]

    async def _get_frequently_bought_together_array(self, limit: int = 5):
        """
        Implementation for orders where order_details is an array
        """
        # Check if there are enough orders with multiple items
        count = await self.orders_collection.count_documents({
            "order_details": {"$exists": True, "$type": "array"},
            "$expr": {"$gt": [{"$size": "$order_details"}, 1]}
        })
        
        if count == 0:
            print("No orders with multiple items found, returning empty list")
            return []
        
        # Use aggregation pipeline to find product pairs frequently purchased together
        pipeline = [
            # First, filter only orders that have order_details as an array
            {
                "$match": {
                    "order_details": { "$exists": True, "$type": "array" }
                }
            },
            # Then filter orders with more than one product
            {
                "$match": {
                    "$expr": { "$gt": [{ "$size": "$order_details" }, 1] }
                }
            },
            # Unwind order details to prepare for pairing
            { "$unwind": "$order_details" },
            # Store the first product info
            {
                "$project": {
                    "_id": 1,
                    "order_id": 1,
                    "product1": "$order_details"
                }
            },
            # Create a copy of the order data
            {
                "$lookup": {
                    "from": "orders",
                    "localField": "order_id",
                    "foreignField": "order_id",
                    "as": "same_order"
                }
            },
            { "$unwind": "$same_order" },
            # Make sure same_order has order_details array
            {
                "$match": {
                    "same_order.order_details": { "$exists": True, "$type": "array" }
                }
            },
            # Unwind the products in the copy
            { "$unwind": "$same_order.order_details" },
            # Create product pairs, filtering to avoid duplicates and counting each pair only once
            {
                "$match": {
                    "$expr": {
                        "$and": [
                            # Products must be different
                            { "$ne": ["$product1.product_id", "$same_order.order_details.product_id"] },
                            # product1 ID < product2 ID to avoid counting the same pair twice
                            { "$lt": ["$product1.product_id", "$same_order.order_details.product_id"] }
                        ]
                    }
                }
            },
            # Create the output structure
            {
                "$project": {
                    "_id": 0,
                    "pair_id": {
                        "$concat": [
                            { "$toString": "$product1.product_id" }, 
                            "_", 
                            { "$toString": "$same_order.order_details.product_id" }
                        ]
                    },
                    "product1": "$product1",
                    "product2": "$same_order.order_details"
                }
            },
            # Count frequency
            {
                "$group": {
                    "_id": "$pair_id",
                    "product_pair": { "$first": { "product1": "$product1", "product2": "$product2" } },
                    "frequency": { "$sum": 1 }
                }
            },
            # Sort by frequency in descending order
            { "$sort": { "frequency": -1 } },
            # Limit the number of results
            { "$limit": limit },
            # Format the final output
            {
                "$project": {
                    "_id": 0,
                    "product_pair": 1,
                    "frequency": 1
                }
            }
        ]
        
        try:
            cursor = self.orders_collection.aggregate(pipeline)
            results = await cursor.to_list(length=limit)
            
            # If no results found, return empty list
            if not results:
                print("No product pairs found via aggregation, returning empty list")
                return []
            
            return results
        except Exception as e:
            print(f"Error getting frequently bought together products: {e}")
            # Return empty list if there's an error
            return []

    async def get_recommended_products(self, category: str = None, limit: int = 5):
        """
        Get recommended products with the lowest prices
        """
        if not self.hardware_collections:
            await self._init_collections()
        
        # Prepare data for search
        hardware_mapping = [
            {"collection_name": "CPUs", "category": "CPU", "id_field": "cpu_id"},
            {"collection_name": "Rams", "category": "RAM", "id_field": "ram_id"},
            {"collection_name": "Mainboards", "category": "Mainboard", "id_field": "mainboard_id"},
            {"collection_name": "GPUs", "category": "GPU", "id_field": "gpu_id"},
            {"collection_name": "Cases", "category": "Case", "id_field": "case_id"},
            {"collection_name": "PSUs", "category": "PSU", "id_field": "psu_id"},
            {"collection_name": "SSDs", "category": "SSD", "id_field": "ssd_id"},
            {"collection_name": "M2s", "category": "M2", "id_field": "m2_id"}
        ]
        
        # Filter by category if specified
        if category:
            hardware_mapping = [hw for hw in hardware_mapping if hw["category"] == category]
            if not hardware_mapping:
                raise HTTPException(status_code=400, detail=f"Invalid product category: '{category}'")
        
        all_products = []
        
        # Find the cheapest products in each category
        for hw in hardware_mapping:
            try:
                # Make sure collection exists in hardware_collections
                if hw["collection_name"] not in self.hardware_collections:
                    print(f"Collection {hw['collection_name']} not found in hardware_collections")
                    continue
                
                # Get the collection reference
                collection = self.hardware_collections.get(hw["collection_name"])
                if collection is None:
                    print(f"Collection {hw['collection_name']} is None")
                    continue
                
                # Check if collection has any data
                count = await collection.count_documents({})
                if count == 0:
                    print(f"No products found for category {hw['category']}")
                    continue
                
                # Find products with prices and sort by price
                cursor = collection.find(
                    {"price": {"$exists": True, "$gt": 0}}, 
                    {"_id": 0}  # Exclude only _id, include all other fields
                ).sort("price", 1).limit(5 if category else 2)
                
                results = await cursor.to_list(length=10)
                
                # Add category field for standardization
                for item in results:
                    item["category"] = hw["category"]
                
                all_products.extend(results)
                
            except Exception as e:
                print(f"Error processing {hw['category']}: {e}")
                continue
        
        # Sort by price ascending
        all_products.sort(key=lambda x: x.get("price", float('inf')))
        
        # If no products found, return an empty list
        if not all_products:
            return []
        
        # Limit to requested number of results
        return all_products[:limit]
