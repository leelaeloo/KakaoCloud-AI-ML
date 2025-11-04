from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from ..models import Order, OrderItem, OrderCreate, OrderStatus, MessageResponse
from ..services import OrderService
from ..dependencies import get_order_service

router = APIRouter(
    prefix="/orders",
    tags=["주문"]
)

@router.post(
    "/", 
    response_model=Order, 
    status_code=status.HTTP_201_CREATED, 
    summary="새로운 주문 생성"
)
def create_order(
    order_data: OrderCreate,
    service: OrderService = Depends(get_order_service)
):
    """
    메뉴 아이템 ID와 수량을 포함하여 새로운 주문을 생성합니다.
    """
    new_order = service.create_order(order_data.items)
    if not new_order:
        raise HTTPException(
            status_code=404, 
            detail="하나 이상의 메뉴 아이템을 찾을 수 없습니다."
        )
    return new_order

@router.get(
    "/", 
    response_model=List[Order], 
    summary="전체 주문 목록 조회"
)
def get_all_orders(service: OrderService = Depends(get_order_service)):
    """
    현재까지 생성된 모든 주문 목록을 조회합니다.
    """
    return service.get_all_orders()

@router.get(
    "/{order_id}", 
    response_model=Order, 
    summary="특정 주문 상세 조회"
)
def get_order(
    order_id: int, 
    service: OrderService = Depends(get_order_service)
):
    """
    ID를 사용하여 특정 주문의 상세 정보를 조회합니다.
    - **order_id**: 조회할 주문의 ID
    """
    order = service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=404, 
            detail="주문을 찾을 수 없습니다."
        )
    return order

@router.patch(
    "/{order_id}/status", 
    response_model=Order, 
    summary="주문 상태 업데이트"
)
def update_order_status(
    order_id: int,
    status: OrderStatus,
    service: OrderService = Depends(get_order_service)
):
    """
    주문의 상태를 'preparing', 'ready', 'completed' 중 하나로 업데이트합니다.
    - **order_id**: 상태를 변경할 주문의 ID
    - **status**: 변경할 주문 상태 (pending, preparing, ready, completed)
    """
    updated_order = service.update_order_status(order_id, status)
    if not updated_order:
        raise HTTPException(
            status_code=404, 
            detail="주문을 찾을 수 없습니다."
        )
    return updated_order

@router.get(
    "/status/{status}",
    response_model=List[Order],
    summary="상태별 주문 목록 조회"
)
def get_orders_by_status(
    status: OrderStatus,
    service: OrderService = Depends(get_order_service)
):
    """
    특정 상태(pending, preparing, ready, completed)에 해당하는 주문 목록을 조회합니다.
    - **status**: 조회할 주문의 상태
    """
    orders = service.get_orders_by_status(status)
    return orders
