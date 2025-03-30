from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import List, Optional
from datetime import datetime, timezone

class ComputerSet(BaseModel):
    cpu_id: int = Field(..., description="CPU ID must start with 1 and have 5 digits")
    ram_id: int = Field(..., description="RAM ID must start with 2 and have 5 digits")
    mainboard_id: int = Field(..., description="Mainboard ID must start with 3 and have 5 digits")
    gpu_id: int = Field(..., description="GPU ID must start with 5 and have 5 digits")
    case_id: int = Field(..., description="Case ID must start with 6 and have 5 digits")
    psu_id: int = Field(..., description="PSU ID must start with 7 and have 5 digits")
    ssd_id: Optional[int] = None
    m2_id: Optional[int] = None

class ShippingDetails(BaseModel):
    user_id: int = Field(..., description="User ID must start with 1 and have 5 digits")
    name: str = Field(..., description="Recipient's name")
    phone: str = Field(..., description="Recipient's phone number")
    email: str = Field(..., pattern=r"^\w+@\w+\.\w+$", description="Recipient's email address")
    shipping_address: str = Field(..., description="Shipping address")
    shipping_status: str = Field(..., description="Shipping status must be either 'Pending', 'Shipped', 'Delivered', or 'Cancelled'")
    note: Optional[str] = Field(..., description="Additional notes for shipping")

class Order(BaseModel):
    order_id: int = Field(..., description="Order ID must have 5 digits")
    user_id: int = Field(..., description="User ID must start with 1 and have 5 digits")
    order_date: datetime = Field(..., description="Order date in UTC timezone")
    total_price: int = Field(..., ge=0, description="Total price must be non-negative")
    status: str = Field(..., description="Order status must be either 'Pending', 'Confirmed', 'Delivered', or 'Cancelled'")
    order_details: ComputerSet = Field(..., description="computer sets in the order")
    shipping_details: ShippingDetails = Field(..., description="shipping details of the order")

    @field_validator('order_id')
    def check_order_id(cls, value):
        if not (10000 <= value <= 99999):
            raise ValueError('Order ID must have 5 digits')
        return value

    @field_validator('user_id')
    def check_user_id(cls, value):
        if not (10000 <= value <= 19999):
            raise ValueError('User ID must start with 1 and have 5 digits')
        return value
    
