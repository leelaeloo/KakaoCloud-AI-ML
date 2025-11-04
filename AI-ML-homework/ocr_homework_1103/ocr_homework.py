import os
import warnings
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

import Levenshtein
import matplotlib.pyplot as plt
import pytesseract
import requests
import fitz  # pyMuPDF
from PIL import Image


# 설정 클래스
@dataclass
class Config:
    """OCR 벤치마크 설정"""

    api_key: str = "K89413360888957"
    pdf_path: str = "samples/ocr_test.pdf"
    ground_truth: str = (
        "OCR 성능 비교를 위한 문서입니다. "
        "1. 금융 분야: 결제 금액 12,500원. 승인 번호 12345678. 감사합니다. "
        "2. 교육 분야: $E=mc^2$ 미분 공식. 다음 문제를 푸시오. "
        "3. 행정 분야: 문서 관리 번호 KOR-2025-001. 발급일 2025.11.03. "
        "신속한 업무 처리를 위한 OCR 기술의 중요성을 확인합니다."
    )
    temp_image_path: str = "temp_test_page1.png"
    output_chart_path: str = "ocr_benchmark_chart.png"
    zoom_factor: int = 4
    snippet_length: int = 40


# 유틸리티 함수
def normalize_text(text: str) -> str:
    """텍스트 정규화: 공백 및 줄바꿈 처리"""
    return text.strip().replace("\n", " ")


def calculate_error_rate(reference: str, hypothesis: str) -> float:
    """
    Levenshtein 거리를 이용한 에러율 계산

    Args:
        reference: 정답 텍스트
        hypothesis: OCR 추출 텍스트

    Returns:
        에러율 (0-100%)
    """
    ref = normalize_text(reference)
    hyp = normalize_text(hypothesis)

    if len(ref) == 0:
        return 100.0 if len(hyp) > 0 else 0.0

    distance = Levenshtein.distance(ref, hyp)
    return (distance / len(ref)) * 100


def cleanup_temp_file(file_path: str) -> None:
    """임시 파일 삭제"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"[INFO] 임시 파일 '{file_path}' 삭제 완료")
    except OSError as e:
        print(f"[WARNING] 임시 파일 삭제 실패: {e}")


# PDF 처리
def convert_pdf_to_image(
    pdf_path: str, output_path: str, zoom: int = 4
) -> Optional[str]:
    """
    PDF 첫 페이지를 고해상도 이미지로 변환

    Args:
        pdf_path: PDF 파일 경로
        output_path: 출력 이미지 경로
        zoom: 확대 배율 (기본값: 4)

    Returns:
        성공 시 이미지 경로, 실패 시 None
    """
    try:
        with fitz.open(pdf_path) as doc:
            page = doc.load_page(0)
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix)
            pix.save(output_path)

        print(f"[SUCCESS] PDF를 이미지로 변환: {output_path}")
        return output_path

    except Exception as e:
        print(f"[ERROR] PDF 변환 실패: {e}")
        return None


# OCR 엔진 인터페이스
class OCREngine:
    """OCR 엔진 추상 클래스"""

    @staticmethod
    def extract_text(source: str, **kwargs) -> Tuple[bool, str]:
        """
        텍스트 추출

        Returns:
            (성공 여부, 추출된 텍스트 또는 에러 메시지)
        """
        raise NotImplementedError


class TesseractOCR(OCREngine):
    """Tesseract OCR 엔진"""

    @staticmethod
    def extract_text(image_path: str, **kwargs) -> Tuple[bool, str]:
        try:
            text = pytesseract.image_to_string(Image.open(image_path), lang="kor+eng")
            return True, text
        except Exception as e:
            return False, f"Tesseract 오류: {e}"


class OCRSpaceAPI(OCREngine):
    """OCR.space API 엔진"""

    API_URL = "https://api.ocr.space/parse/image"

    @staticmethod
    def extract_text(image_path: str, api_key: str, **kwargs) -> Tuple[bool, str]:
        try:
            payload = {
                "apikey": api_key,
                "language": "kor",
                "isOverlayRequired": False,  # 오버레이 비활성화
                "OCREngine": "2",  # 엔진 2 사용
                "scale": True,  # 자동 스케일링
            }

            with open(image_path, "rb") as f:
                response = requests.post(
                    OCRSpaceAPI.API_URL,
                    files={"file": f},
                    data=payload,
                    timeout=60,  # 타임아웃 증가
                )

            result = response.json()

            if "ParsedResults" in result and result["ParsedResults"]:
                text = result["ParsedResults"][0].get("ParsedText", "")
                # 에러 체크
                if result.get("IsErroredOnProcessing"):
                    error_detail = result.get("ErrorMessage", "알 수 없는 처리 오류")
                    print(f"[WARNING] OCR-Space 처리 중 오류: {error_detail}")
                return True, text

            error_msg = result.get("ErrorMessage", "알 수 없는 오류")
            return False, f"OCR-Space 오류: {error_msg}"

        except requests.RequestException as e:
            return False, f"OCR-Space 네트워크 오류: {e}"
        except Exception as e:
            return False, f"OCR-Space 오류: {e}"


class PyMuPDFOCR(OCREngine):
    """pyMuPDF 디지털 텍스트 추출"""

    @staticmethod
    def extract_text(pdf_path: str, **kwargs) -> Tuple[bool, str]:
        try:
            text_parts = []
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    text_parts.append(page.get_text())

            return True, "".join(text_parts)

        except Exception as e:
            return False, f"pyMuPDF 오류: {e}"


# 시각화
def create_comparison_chart(error_results: Dict[str, float], output_path: str) -> None:
    """
    OCR 엔진 비교 차트 생성

    Args:
        error_results: {엔진명: 에러율} 딕셔너리
        output_path: 출력 파일 경로
    """
    engine_names = list(error_results.keys())
    error_rates = list(error_results.values())

    colors = ["#3498DB", "#2ECC71", "#E74C3C"]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(engine_names, error_rates, color=colors[: len(engine_names)])

    # 막대 위에 값 표시
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.5,
            f"{height:.2f}%",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
        )

    plt.title(
        "OCR Engine Performance Comparison (Levenshtein Distance)",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )
    plt.ylabel("Error Rate (%)", fontsize=12)
    plt.xlabel("OCR Engine", fontsize=12)
    plt.ylim(0, max(error_rates) * 1.2 if max(error_rates) > 0 else 10)
    plt.grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[SUCCESS] 비교 차트 저장: {output_path}")


# 메인 실행 로직
class OCRBenchmark:
    """OCR 벤치마크 실행 클래스"""

    def __init__(self, config: Config):
        self.config = config
        self.results = {}
        self.extracted_texts = {}  # OCR 추출 텍스트 저장

    def validate_files(self) -> bool:
        """필수 파일 존재 확인"""
        if not os.path.exists(self.config.pdf_path):
            print(f"[ERROR] PDF 파일을 찾을 수 없습니다: {self.config.pdf_path}")
            return False
        return True

    def run(self) -> None:
        """벤치마크 실행"""
        print("=" * 70)
        print(f"{'OCR 벤치마크 시작':^70}")
        print("=" * 70)
        print(f"대상 파일: {self.config.pdf_path}\n")

        if not self.validate_files():
            return

        # PDF를 이미지로 변환
        image_path = convert_pdf_to_image(
            self.config.pdf_path, self.config.temp_image_path, self.config.zoom_factor
        )

        if not image_path:
            print("[ERROR] PDF 변환 실패로 벤치마크를 중단합니다")
            return

        try:
            # OCR 실행
            self._run_ocr_engines(image_path)

            # 결과 출력
            self._print_results()

            # 차트 생성
            if self.results:
                create_comparison_chart(self.results, self.config.output_chart_path)

        finally:
            # 정리
            cleanup_temp_file(self.config.temp_image_path)

    def _run_ocr_engines(self, image_path: str) -> None:
        """모든 OCR 엔진 실행"""
        print("\n" + "-" * 70)
        print("OCR 엔진 실행 중...")
        print("-" * 70)

        # 1. pyMuPDF (디지털 텍스트 추출)
        success, text = PyMuPDFOCR.extract_text(self.config.pdf_path)
        if success:
            error_rate = calculate_error_rate(self.config.ground_truth, text)
            self.results["pyMuPDF"] = error_rate
            self.extracted_texts["pyMuPDF"] = text
            print(f"✓ pyMuPDF 완료: {error_rate:.2f}%")
        else:
            print(f"✗ pyMuPDF 실패: {text}")

        # 2. Tesseract (이미지 OCR)
        success, text = TesseractOCR.extract_text(image_path)
        if success:
            error_rate = calculate_error_rate(self.config.ground_truth, text)
            self.results["Tesseract"] = error_rate
            self.extracted_texts["Tesseract"] = text
            print(f"✓ Tesseract 완료: {error_rate:.2f}%")
        else:
            print(f"✗ Tesseract 실패: {text}")

        # 3. OCR.space API (이미지 OCR)
        success, text = OCRSpaceAPI.extract_text(image_path, self.config.api_key)
        if success:
            error_rate = calculate_error_rate(self.config.ground_truth, text)
            self.results["OCR-Space"] = error_rate
            self.extracted_texts["OCR-Space"] = text
            print(f"✓ OCR-Space 완료: {error_rate:.2f}%")
        else:
            print(f"✗ OCR-Space 실패: {text}")

    def _print_results(self) -> None:
        """결과 출력"""
        print("\n" + "=" * 70)
        print(f"{'최종 결과':^70}")
        print("=" * 70)

        if not self.results:
            print("결과가 없습니다. 모든 OCR 엔진이 실패했습니다.")
            return

        # 오류율 기준 정렬
        sorted_results = sorted(self.results.items(), key=lambda x: x[1])

        for rank, (engine, error_rate) in enumerate(sorted_results, 1):
            status = "1. " if rank == 1 else "2. " if rank == 2 else "3. "
            print(f"{status} {engine:15s}: {error_rate:6.2f}%")

        print("=" * 70)

        # 추출된 텍스트 출력
        self._print_extracted_texts()

    def _print_extracted_texts(self) -> None:
        """OCR로 추출된 텍스트 출력"""
        if not self.extracted_texts:
            return

        print("\n" + "=" * 70)
        print(f"{'추출된 텍스트 비교':^70}")
        print("=" * 70)

        # 정답 텍스트
        print(f"\n[정답 (Ground Truth)]")
        print("-" * 70)
        print(self.config.ground_truth)

        # 각 엔진의 추출 결과
        for engine_name in ["pyMuPDF", "Tesseract", "OCR-Space"]:
            if engine_name in self.extracted_texts:
                text = self.extracted_texts[engine_name]
                normalized_text = normalize_text(text)

                print(f"\n[{engine_name} 추출 결과]")
                print("-" * 70)

                # 전체 텍스트 출력
                if normalized_text:
                    print(normalized_text)
                else:
                    print("(텍스트 없음)")

        print()
        print("=" * 70)


# 실행
def main():
    """메인 함수"""
    # 설정 로드
    config = Config()

    # 벤치마크 실행
    benchmark = OCRBenchmark(config)
    benchmark.run()


if __name__ == "__main__":
    main()
