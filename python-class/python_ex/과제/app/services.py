from typing import List, Optional
from .models import MenuItem, Order, OrderCreate, OrderStatus, UserCreate, UserResponse, DrinkCategory
from . import crud

class MenuService:
    async def get_all_menu_items(self) -> List[MenuItem]:
        return crud.get_all_menu_items()
    
    async def get_menu_item(self, item_id: int) -> Optional[MenuItem]:
        return crud.get_menu_item_by_id(item_id)

    async def get_menu_by_category(self, category: DrinkCategory) -> List[MenuItem]:
        all_items = crud.get_all_menu_items()
        return [item for item in all_items if item.category == category]

class OrderService:
    def __init__(self):
        self.orders = crud.db_orders
        
    async def create_order(self, order_data: OrderCreate) -> Order:
        total_price = 0
        items_in_order = []
        
        for item in order_data.items:
            menu_item = crud.get_menu_item_by_id(item.item_id)
            if not menu_item:
                raise ValueError(f"메뉴 아이템 ID {item.item_id}를 찾을 수 없습니다.")
            total_price += menu_item.price * item.quantity
            items_in_order.append(item)
            
        return crud.create_new_order(items_in_order, total_price)

    async def get_order(self, order_id: int) -> Optional[Order]:
        return crud.get_order_by_id(order_id)

    async def get_orders_by_status(self, status_filter: OrderStatus) -> List[Order]:
        return crud.get_orders_by_status(status_filter)

    async def update_order_status(self, order_id: int, new_status: OrderStatus) -> Optional[Order]:
        return crud.update_order_status(order_id, new_status)

class UserService:
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        return crud.create_new_user(user_data.username, user_data.email)
    
    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        return crud.get_user_by_id(user_id)
