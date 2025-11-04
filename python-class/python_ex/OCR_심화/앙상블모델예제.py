import cv2
import numpy as np
import easyocr
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
from typing import List, Dict, Tuple, Union, Optional
import re

class KoreanOCREnsemble:

    def __init__(self, use_gpu: bool = True) -> None:
        print("한글 앙상블 OCR 시스템 초기화 중 ...")

        self.device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
        print(f"Device: {self.device}")

        try:
            self.easy_ocr = easyocr.Reader(
                ['ko', 'en'],
                gpu=use_gpu
            )
            print("EasyOCR 초기화 완료")
        except Exception as e:
            print(f"EasyOCR 초기화 실패: {e}")
            self.easy_ocr = None

        try:
            model_name = "microsoft/trocr-base-printed"
            self.trocr_processor = TrOCRProcessor.from_pretrained(model_name)
            self.trocr_model = VisionEncoderDecoderModel.from_pretrained(model_name)

            if use_gpu and torch.cuda.is_available():
                self.trocr_model.to(self.device)

            print("TrOCR 초기화 완료 (직접 모델 방식)")

        except Exception as e:
            print(f"TrOCR 초기화 실패: {e}")
            self.trocr_processor = None
            self.trocr_model = None

        print("앙상블 OCR 시스템 준비 완료")

    def extract_text_easy(self, image: np.ndarray) -> List[Dict]:
        if self.easy_ocr is None:
            return []
        try:
            results = self.easy_ocr.readtext(image)

            extracted_texts = []
            for result in results:
                bbox, text, confidence = result
                extracted_texts.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox,
                    'engine': 'EasyOCR'
                })
            print(f"EasyOCR 인식 결과: {extracted_texts}")

            return extracted_texts
        
        except Exception as e:
            print(f"EasyOCR 오류: {e}")
            return []
        
    def extract_text_trocr(self, image: np.ndarray) -> List[Dict]:
        if self.trocr_processor is None or self.trocr_model is None:
            return []
        
        try:
            from PIL import Image

            if isinstance(image, np.ndarray):
                image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                image_pil = image

            pixel_values = self.trocr_processor(image_pil, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)

            with torch.no_grad():
                outputs = self.trocr_model.generate(
                    pixel_values,
                    return_dict_in_generate=True,
                    output_scores=True,
                    max_length=256
                )
                generated_ids = outputs.sequences
                token_scores = outputs.scores

                if token_scores:
                    token_probs = []
                    for score in token_scores:
                        probs = torch.softmax(score, dim=-1)
                        max_prob = torch.max(probs).item()
                        token_probs.append(max_prob)

                    confidence = sum(token_probs) / len(token_probs) if token_probs else 0.0
                else:
                    confidence = 0.0

                text = self.trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

                print(f"TrOCR 인식 결과: {text}")

                return [{
                    'text': text,
                    'confidence': confidence,
                    'bbox': None,
                    'engine': 'TrOCR'
                }] if text.strip() else []
            
        except Exception as e:
            print(f"TrOCR 오류: {e}")
            import traceback
            traceback.print_exc()
            return []
        
    def is_korean_text(self, text: str) -> float:
        if not text:
            return 0.0
        
        korean_chars = sum(1 for char in text if 0xAC00 <= ord(char) <= 0xD7A3)

        return korean_chars / len(text)
    
    def is_english_text(self, text: str) -> float:
        if not text:
            return 0.0
        
        total_chars = len([c for c in text if c.isalpha()])
        if total_chars == 0:
            return 0.0
        
        english_chars = sum(1 for char in text if char.isalpha() and ord(char) < 128)

        ratio = english_chars / total_chars

        if re.search(r'[A-Z][a-z]', text):
            ratio = min(1.0, ratio + 0.1)

        return ratio
    
    def filter_and_merge_results(self,
                                easy_results: List[Dict],
                                trocr_results: List[Dict]) -> List[Dict]:
        
        all_results = []

        for result in easy_results:
            english_ratio = self.is_english_text(result['text'])
            korean_ratio = self.is_korean_text(result['text'])

            if korean_ratio > 0.5:
                result['priority'] = 'high'
                result['reason'] = 'Korean text - EasyOCR high'

            elif english_ratio > 0.5:
                result['priority'] = 'low'
                result['reason'] = 'English text - EasyOCR low'

            elif korean_ratio > 0.2 and english_ratio > 0.2:
                result['priority'] = 'high'
                result['reason'] = 'Mixed text - EasyOCR high'

            else:
                result['priority'] = 'high'
                result['reason'] = 'EasyOCR default'

            all_results.append(result)

        for result in trocr_results:
            english_ratio = self.is_english_text(result['text'])
            korean_ratio = self.is_korean_text(result['text'])

            if english_ratio > 0.5 and korean_ratio < 0.5:
                result['confidence'] = min(1.0, result['confidence'] + 0.1)
                result['priority'] = 'very_high'
                result['reason'] = 'English text - TrOCR specialized'
                all_results.append(result)

            elif not self._is_duplicate_text(result['text'], all_results):
                result['priority'] = 'low'
                result['reason'] = 'TrOCR supplementary'
                all_results.append(result)

        final_results = []
        for result in all_results:
            best_existing = None
            for existing in final_results:
                if self._calculate_text_similarity(result['text'], existing['text']) > 0.8:
                    best_existing = existing
                    break

            if best_existing is None:
                final_results.append(result)
            else:
                should_replace = self._should_replace_result(result, best_existing)
                if should_replace:
                    final_results.remove(best_existing)
                    final_results.append(result)

        def get_priority_score(priority):
            if priority == 'very_high': return 0
            elif priority == 'high': return 1
            elif priority == 'medium': return 2
            else: return 3

        final_results.sort(key=lambda x: (
            get_priority_score(x['priority']),
            -x['confidence']
        ))

        print(f"final_results: {final_results}")

        print(f"\n정렬 결과 미리보기:")
        for i, result in enumerate(final_results):
            priority_score = get_priority_score(result['priority'])
            print(f"[{i+1}]. [{result['engine']}] '{result['text']}' ")
            print(f"우선순위: {result['priority']}({priority_score}), 신뢰도: {result['confidence']:.2f}")
        
        return final_results

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:

        # 두 텍스트 간 유사도 계산

        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _should_replace_result(self, new_result: Dict, existing_result: Dict) -> bool:
        """
        중복된 텍스트에서 어떤 결과를 사용할지 결정
        """
        # 우선순위 점수 계산 (very_high 추가)
        priority_scores = {'very_high': 4, 'high': 3, 'medium': 2, 'low': 1}
        
        new_priority_score = priority_scores.get(new_result['priority'], 0)
        existing_priority_score = priority_scores.get(existing_result['priority'], 0)
        
        # 1. 우선순위가 다르면 높은 것 선택
        if new_priority_score > existing_priority_score:
            return True
        elif new_priority_score < existing_priority_score:
            return False
        
        # 2. 우선순위가 같으면 신뢰도로 비교
        # 영어 텍스트에서 TrOCR에게 추가 혜택 제공
        english_ratio = self.is_english_text(new_result['text'])
        korean_ratio = self.is_korean_text(new_result['text'])

        new_confidence = new_result['confidence']
        existing_confidence = existing_result['confidence']

        # 영어 텍스트일 때 TrOCR에게 보너스 (교체 결정에서만)
        if english_ratio > 0.5 and korean_ratio < 0.5:
            if new_result['engine'] == 'TrOCR':
                new_confidence += 0.15  # 15% 보너스
            if existing_result['engine'] == 'TrOCR':
                existing_confidence += 0.15

        if new_confidence > existing_confidence + 0.05:  # 5% 이상 차이
            return True
        elif existing_confidence > new_confidence + 0.05:
            return False
        
        # 3. 신뢰도도 비슷하면 엔진별 특성 고려
        # 영어 텍스트면 TrOCR 우선 (임계값 낮춤)
        if english_ratio > 0.5 and korean_ratio < 0.5:
            return new_result['engine'] == 'TrOCR'
        # 한글 텍스트면 EasyOCR 우선
        elif korean_ratio > 0.5:
            return new_result['engine'] == 'EasyOCR'
        # 혼용이면 신뢰도로만 판단 (이미 위에서 처리됨)
        else:
            return False

    def _is_duplicate_text(self, text: str, existing_results: List[Dict], threshold: float = 0.8) -> bool:

        # 텍스트 중복 여부 확인

        for existing in existing_results:
            # 유사도 계산 및 중복 판단
            similarity = self._calculate_text_similarity(text, existing['text'])
            # 유사도가 임계값 이상이면 중복으로 판단
            if similarity > threshold:
                return True
        return False

    def extract_text_ensemble(self, image_path: Union[str, np.ndarray]) -> Dict:

        # 앙상블 OCR 수행

        # 이미지 로드
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:
            image = image_path

        if image is None:
            return {"error": "이미지를 로드할 수 없습니다"}

        # 각 엔진별 텍스트 추출
        print("각 OCR 엔진 실행 중...")

        easy_results = self.extract_text_easy(image)
        print(f"easy_results: {easy_results}")
        print(f" = EasyOCR: {len(easy_results)}개 텍스트 발견")

        trocr_results = self.extract_text_trocr(image)
        print(f"trocr_results: {trocr_results}")
        print(f" = TrOCR: {len(trocr_results)}개 텍스트 발견")

        merged_results = self.filter_and_merge_results(
            easy_results, trocr_results
        )

        final_text = " ".join([result['text'] for result in merged_results
                               if result['confidence'] > 0.5])
        
        return {
            'final_text': final_text,
            'detailed_results': merged_results,
            'engine_stats': {
                'easy_count': len(easy_results),
                'trocr_count': len(trocr_results),
                'merged_count': len(merged_results)
            }
        }


def create_korean_test_image() -> List[np.ndarray]:

    # 한글 OCR 테스트용 이미지 생성
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np

    try:
        font_large = ImageFont.truetype("malgun.ttf", 40)
        font_medium = ImageFont.truetype("malgun.ttf", 30)
    except:
        try:
            font_large = ImageFont.truetype("arial.ttf", 40)
            font_medium = ImageFont.truetype("arial.ttf", 30)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()

    texts = [
        "한글 OCR 성능 테스트",
        "Korean OCR Performance Test",
        "혼용 텍스트 Mixed Text 처리",
        "인공지능 AI 기술 Technology",
        "숫자 테스트 : 2024년 12월",
        "This is a test of English text"
    ]

    img_list = []
    for i, text in enumerate(texts):
        img = Image.new('RGB', (800, 400), 'white')
        draw = ImageDraw.Draw(img)
        # 텍스트 크기에 따라 폰트 선택
        font = font_large if i == 0 else font_medium
        draw.text((50, 150), text, fill='black', font=font)
        
        # PNG 파일로 저장 (선택사항)
        img.save(f"test_image_{i+1}.png")
        
        # BGR로 변환하여 리스트에 추가
        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img_list.append(img_bgr)
    
    return img_list


def korean_ocr_demo() -> Tuple[KoreanOCREnsemble, List[Dict]]:

    # 한글 앙상블 OCR 데모 실행
    print("한글 앙상블 OCR 데모 - 다중 이미지 처리")

    ocr_ensemble = KoreanOCREnsemble(use_gpu=True)

    test_images = create_korean_test_image()

    all_results = []

    test_texts = [
        "한글 OCR 성능 테스트",
        "Korean OCR Performance Test",
        "혼용 텍스트 Mixed Text 처리",
        "인공지능 AI 기술 Technology",
        "숫자 테스트 : 2024년 12월",
        "This is a test of English text"
    ]

    for i, (test_image, expected_text) in enumerate(zip(test_images, test_texts)):
        print(f"\n=== 이미지 {i+1} 처리 중 ===")
        result = ocr_ensemble.extract_text_ensemble(test_image)
        result['image_index'] = i + 1
        result['expected_text'] = expected_text
        all_results.append(result)

        print(f"\n최종 결과:")
        print(f" 예상 텍스트: '{expected_text}'")
        print(f" 추출된 텍스트: '{result['final_text']}'")

        print(f"\n엔진별 통계:")
        stats = result['engine_stats']
        print(f" = EasyOCR: {stats['easy_count']}개")
        print(f" = TrOCR: {stats['trocr_count']}개")
        print(f" = 병합: {stats['merged_count']}개")

        print(f"\n상세 결과:")
        for j, detail in enumerate(result['detailed_results']):
            print(f" {j+1}. [{detail['engine']}] '{detail['text']}' "
                  f"(신뢰도: {detail['confidence']:.2f}, 우선순위: {detail['priority']})")
            
    return ocr_ensemble, all_results


if __name__ == "__main__":
    ocr_system, results = korean_ocr_demo()