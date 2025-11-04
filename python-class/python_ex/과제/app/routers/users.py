from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models import UserResponse, UserCreate
from ..services import UserService
from ..dependencies import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["사용자"]
)

@router.post("/", response_model=UserResponse, summary="새로운 사용자 생성")
def create_user(
    user: UserCreate, 
    service: UserService = Depends(get_user_service)
):
    """
    새로운 사용자 계정을 생성합니다.
    - **username**: 사용자의 이름
    - **email**: 사용자의 이메일 주소
    """
    new_user = service.create_user(user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse, summary="특정 사용자 조회")
def get_user(
    user_id: int, 
    service: UserService = Depends(get_user_service)
):
    """
    ID를 사용하여 특정 사용자의 정보를 조회합니다.
    - **user_id**: 조회할 사용자의 ID
    """
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user
