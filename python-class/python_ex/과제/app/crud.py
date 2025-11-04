from typing import List, Dict, Optional
from ..models import DrinkCategory, OrderStatus, Order, UserResponse, UserCreate
import copy

# 임시 데이터베이스
db_menu: List[Dict] = [
    {"id": 1, "name": "아메리카노", "price": 4000, "description": "에스프레소에 물을 섞은 기본 커피", "category": "coffee"},
    {"id": 2, "name": "카페 라떼", "price": 4500, "description": "에스프레소와 부드러운 우유의 조합", "category": "latte"},
    {"id": 3, "name": "카라멜 마키아또", "price": 5000, "description": "달콤한 카라멜 시럽이 더해진 라떼", "category": "latte"},
    {"id": 4, "name": "녹차 라떼", "price": 4800, "description": "진한 녹차 풍미의 라떼", "category": "tea"},
    {"id": 5, "name": "딸기 에이드", "price": 5500, "description": "상큼한 딸기맛 에이드", "category": "ade"},
]

db_orders: List[Dict] = []
next_order_id = 1

db_users: List[Dict] = []
next_user_id = 1

# 메뉴 관련 CRUD 함수
def get_all_menu_items() -> List[Dict]:
    """모든 메뉴 아이템을 반환합니다."""
    return copy.deepcopy(db_menu)

def get_menu_item_by_id(item_id: int) -> Optional[Dict]:
    """ID로 특정 메뉴 아이템을 찾아서 반환합니다."""
    for item in db_menu:
        if item["id"] == item_id:
            return copy.deepcopy(item)
    return None

def get_menu_by_category(category: DrinkCategory) -> List[Dict]:
    """카테고리로 메뉴 아이템 목록을 필터링하여 반환합니다."""
    return [copy.deepcopy(item) for item in db_menu if item["category"] == category]

# 주문 관련 CRUD 함수
def create_new_order(items: List[Dict], total_price: int, estimated_time: int) -> Dict:
    """새로운 주문을 생성하고 데이터베이스에 추가합니다."""
    global next_order_id
    new_order = {
        "order_id": next_order_id,
        "items": copy.deepcopy(items),
        "total_price": total_price,
        "status": OrderStatus.pending,
        "estimated_time": estimated_time
    }
    db_orders.append(new_order)
    next_order_id += 1
    return copy.deepcopy(new_order)

def get_order_by_id(order_id: int) -> Optional[Dict]:
    """ID로 특정 주문을 찾아서 반환합니다."""
    for order in db_orders:
        if order["order_id"] == order_id:
            return copy.deepcopy(order)
    return None

def update_order_status(order_id: int, status: OrderStatus) -> Optional[Dict]:
    """주문의 상태를 업데이트합니다."""
    for order in db_orders:
        if order["order_id"] == order_id:
            order["status"] = status
            return copy.deepcopy(order)
    return None

def get_orders_by_status(status: OrderStatus) -> List[Dict]:
    """상태별로 주문 목록을 조회합니다."""
    return [copy.deepcopy(order) for order in db_orders if order["status"] == status]

def get_all_orders() -> List[Dict]:
    """모든 주문을 반환합니다."""
    return copy.deepcopy(db_orders)

# 사용자 관련 CRUD 함수
def create_new_user(user_data: UserCreate) -> Dict:
    """새로운 사용자를 생성하고 데이터베이스에 추가합니다."""
    global next_user_id
    new_user = {
        "user_id": next_user_id,
        "username": user_data.username,
        "email": user_data.email
    }
    db_users.append(new_user)
    next_user_id += 1
    return copy.deepcopy(new_user)

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """ID로 특정 사용자를 찾아서 반환합니다."""
    for user in db_users:
        if user["user_id"] == user_id:
            return copy.deepcopy(user)
    return None
