from pydantic import BaseModel
from typing import List, Union
from enum import Enum

class DrinkCategory(str, Enum):
    coffee = "coffee"
    latte = "latte"
    tea = "tea"
    ade = "ade"

class MenuItem(BaseModel):
    id: int
    name: str
    price: int
    description: Union[str, None] = None
    category: DrinkCategory

class OrderItem(BaseModel):
    item_id: int
    quantity: int

class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"
    completed = "completed"

class OrderCreate(BaseModel):
    items: List[OrderItem]

class Order(BaseModel):
    order_id: int
    items: List[OrderItem]
    total_price: int
    status: OrderStatus = OrderStatus.pending
    estimated_time: int = 15

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str

class MessageResponse(BaseModel):
    message: str
    details: dict
