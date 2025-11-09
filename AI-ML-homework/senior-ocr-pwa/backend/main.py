from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
import os
import uuid
from datetime import datetime
from typing import Dict, List
import json

from database import get_db, init_db
from models import OCRHistory

# FastAPI 앱 생성
app = FastAPI(
    title="시니어 친화 OCR API",
    description="간단하고 쉬운 OCR 서비스",
    version="1.0.0"
)

# CORS 설정 (Next.js에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 앱 시작 시 DB 초기화
@app.on_event("startup")
async def startup_event():
    """앱 시작 시 데이터베이스 테이블 생성"""
    await init_db()
    print("✅ 데이터베이스 초기화 완료")

# 디렉토리 설정
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
RESULTS_DIR = os.getenv("RESULTS_DIR", "./results")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


# === 이미지 전처리 함수 ===
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """이미지 전처리 (선명하게 만들기)"""
    # 바이트를 OpenCV 이미지로 변환
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 노이즈 제거
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    # 이진화 (흑백으로)
    binary = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    return binary


# === OCR 함수 ===
def extract_text(image_bytes: bytes, lang: str = "kor+eng") -> Dict:
    """텍스트 추출"""
    try:
        # 이미지 전처리
        processed_img = preprocess_image(image_bytes)

        # OCR 실행
        text = pytesseract.image_to_string(
            processed_img,
            lang=lang,
            config='--oem 3 --psm 6'
        )

        # 상세 정보 추출
        data = pytesseract.image_to_data(
            processed_img,
            lang=lang,
            output_type=pytesseract.Output.DICT
        )

        # 신뢰도 계산
        confidences = [float(c) for c in data['conf'] if c != '-1']
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        # 단어 정보
        words = []
        for i, word in enumerate(data['text']):
            if word.strip():
                words.append({
                    'text': word,
                    'confidence': float(data['conf'][i])
                })

        return {
            'text': text.strip(),
            'confidence': round(avg_confidence, 2),
            'word_count': len(words),
            'words': words
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR 처리 실패: {str(e)}")


# === API 엔드포인트 ===

@app.get("/")
async def root():
    """헬스 체크"""
    return {
        "status": "ok",
        "message": "시니어 친화 OCR API 실행 중",
        "version": "1.0.0"
    }


@app.post("/api/ocr")
async def process_ocr(
    file: UploadFile = File(...),
    language: str = "kor+eng",
    db: AsyncSession = Depends(get_db)
):
    """
    OCR 처리 API
    - 이미지 업로드
    - 텍스트 추출
    - 결과 DB 저장
    - 결과 반환
    """
    try:
        # 파일 타입 검증
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="이미지 파일만 업로드 가능합니다"
            )

        # 파일 읽기
        image_bytes = await file.read()

        # 파일 크기 체크 (10MB)
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="파일 크기는 10MB 이하여야 합니다"
            )

        # 고유 ID 생성
        task_id = str(uuid.uuid4())

        # 원본 이미지 저장 (파일 시스템)
        image_path = os.path.join(UPLOAD_DIR, f"{task_id}.jpg")
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        # OCR 처리
        result = extract_text(image_bytes, language)

        # 결과 데이터 구성
        result_data = {
            'task_id': task_id,
            'timestamp': datetime.now().isoformat(),
            'filename': file.filename,
            'language': language,
            **result
        }

        # JSON 파일로도 저장 (백업용)
        result_path = os.path.join(RESULTS_DIR, f"{task_id}.json")
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        # ✨ DB에 저장
        ocr_record = OCRHistory(
            task_id=task_id,
            text=result['text'],
            word_count=result['word_count'],
            confidence=result['confidence'],
            created_at=datetime.utcnow()
        )
        db.add(ocr_record)
        await db.commit()
        await db.refresh(ocr_record)

        return JSONResponse(content={
            'success': True,
            'task_id': task_id,
            'data': result_data
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"서버 오류: {str(e)}"
        )


@app.get("/api/result/{task_id}")
async def get_result(task_id: str):
    """OCR 결과 조회"""
    try:
        result_path = os.path.join(RESULTS_DIR, f"{task_id}.json")

        if not os.path.exists(result_path):
            raise HTTPException(
                status_code=404,
                detail="결과를 찾을 수 없습니다"
            )

        with open(result_path, "r", encoding="utf-8") as f:
            result = json.load(f)

        return JSONResponse(content={
            'success': True,
            'data': result
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"서버 오류: {str(e)}"
        )


@app.get("/api/history")
async def get_history(limit: int = 10, db: AsyncSession = Depends(get_db)):
    """최근 OCR 기록 조회 (DB에서)"""
    try:
        # DB에서 최신순으로 조회
        query = select(OCRHistory).order_by(desc(OCRHistory.created_at)).limit(limit)
        result = await db.execute(query)
        records = result.scalars().all()

        # 응답 데이터 구성
        history = []
        for record in records:
            history.append({
                'id': record.id,
                'task_id': record.task_id,
                'text_preview': record.text[:100] + '...' if len(record.text) > 100 else record.text,
                'text': record.text,  # 전체 텍스트도 포함
                'confidence': record.confidence,
                'word_count': record.word_count,
                'created_at': record.created_at.isoformat()
            })

        return JSONResponse(content={
            'success': True,
            'count': len(history),
            'data': history
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"서버 오류: {str(e)}"
        )


@app.delete("/api/history/{record_id}")
async def delete_history(record_id: int, db: AsyncSession = Depends(get_db)):
    """OCR 기록 삭제"""
    try:
        # DB에서 레코드 찾기
        query = select(OCRHistory).where(OCRHistory.id == record_id)
        result = await db.execute(query)
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(
                status_code=404,
                detail="기록을 찾을 수 없습니다"
            )

        # 삭제
        await db.delete(record)
        await db.commit()

        return JSONResponse(content={
            'success': True,
            'message': '기록이 삭제되었습니다'
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"서버 오류: {str(e)}"
        )


@app.get("/api/history/{record_id}")
async def get_history_detail(record_id: int, db: AsyncSession = Depends(get_db)):
    """특정 OCR 기록 상세 조회"""
    try:
        # DB에서 레코드 찾기
        query = select(OCRHistory).where(OCRHistory.id == record_id)
        result = await db.execute(query)
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(
                status_code=404,
                detail="기록을 찾을 수 없습니다"
            )

        return JSONResponse(content={
            'success': True,
            'data': {
                'id': record.id,
                'task_id': record.task_id,
                'text': record.text,
                'confidence': record.confidence,
                'word_count': record.word_count,
                'created_at': record.created_at.isoformat()
            }
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"서버 오류: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
