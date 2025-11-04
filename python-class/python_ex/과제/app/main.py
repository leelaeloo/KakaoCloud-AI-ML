from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import MessageResponse
from .routers.menu import menu_router
from .routers.orders import order_router
from .routers.users import user_router

# FastAPI 앱 초기화
app = FastAPI(
    title="카페 주문 관리 시스템",
    description="FastAPI를 사용한 카페 주문 관리 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(user_router)

# 루트 엔드포인트
@app.get("/", response_model=MessageResponse, summary="API 상태 확인")
async def root():
    """API 서버 상태를 확인합니다."""
    return MessageResponse(
        message="카페 주문 관리 시스템 API가 정상적으로 작동 중입니다!",
        details={
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "endpoints": {
                "메뉴 조회": "GET /menu",
                "특정 메뉴": "GET /menu/{item_id}",
                "주문 생성": "POST /orders",
                "주문 조회": "GET /orders/{order_id}",
                "사용자 생성": "POST /users",
                "사용자 조회": "GET /users/{user_id}",
            }
        }
    )