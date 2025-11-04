from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models import MenuItem, DrinkCategory
from ..services import MenuService
from ..dependencies import get_menu_service

router = APIRouter(
    prefix="/menu",
    tags=["메뉴"]
)

@router.get("/", response_model=List[MenuItem], summary="전체 메뉴 조회")
def get_all_menu(service: MenuService = Depends(get_menu_service)):
    """
    카페에서 제공하는 모든 음료 메뉴를 조회합니다.
    """
    return service.get_all_menu_items()

@router.get("/{item_id}", response_model=MenuItem, summary="특정 메뉴 아이템 조회")
def get_menu_item(item_id: int, service: MenuService = Depends(get_menu_service)):
    """
    ID를 사용하여 특정 메뉴 아이템의 상세 정보를 조회합니다.
    - **item_id**: 조회할 메뉴 아이템의 ID
    """
    item = service.get_menu_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="메뉴 아이템을 찾을 수 없습니다.")
    return item

@router.get("/category/{category}", response_model=List[MenuItem], summary="카테고리별 메뉴 조회")
def get_menu_by_category(category: DrinkCategory, service: MenuService = Depends(get_menu_service)):
    """
    음료 카테고리로 메뉴를 조회합니다.
    - **category**: coffee, latte, tea, ade 중 하나
    """
    items = service.get_menu_by_category(category)
    if not items:
        raise HTTPException(status_code=404, detail="해당 카테고리의 메뉴가 없습니다.")
    return items