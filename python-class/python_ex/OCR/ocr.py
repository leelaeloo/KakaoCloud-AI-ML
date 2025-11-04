import pytesseract
from PIL import Image

# 이미지 파일 열기
img = Image.open('example.png')

# OCR 수행 (이미지에서 텍스트 추출)
text = pytesseract.image_to_string(img, lang='kor+eng')

# 결과 출력
print(text)