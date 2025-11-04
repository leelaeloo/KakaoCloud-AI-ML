from .services import MenuService, OrderService, UserService

def get_menu_service():
    return MenuService()

def get_order_service():
    return OrderService()

def get_user_service():
    return UserService()
