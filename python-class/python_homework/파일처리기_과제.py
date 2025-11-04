import os
import sys
import json
import csv
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("과제_로깅.log", encoding='utf-8'),
        logging.StreamHandler(stream=sys.stdout)
    ]
)

# 사용자 정의 예외 계층 구조
class FileProcessingError(Exception):
    # 파일 처리 관련 최상위 사용자 정의 예외
    pass

class InvalidFileFormatError(FileProcessingError):
    # 파일 형식이 올바르지 않을 때 발생하는 예외
    pass

class CustomPermissionError(FileProcessingError):
    # 파일에 대한 접근 권한이 없을 때 발생하는 예외
    pass

# --- 다양한 파일(텍스트, CSV, JSON, 바이너리) 읽고 쓰기 ---
# 텍스트 파일 처리 함수
def process_text_file(filename):
    # 텍스트 파일을 읽어 내용을 반환
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"파일을 찾을 수 없습니다: {filename}")
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")
    except PermissionError:
        logging.error(f"권한 오류: '{filename}' 파일에 접근할 수 없습니다.")
        raise CustomPermissionError(f"파일에 대한 접근 권한이 없습니다: {filename}")

# JSON 파일 처리 함수
def process_json_file(filename):
    # JSON 파일을 읽어 파이썬 객체(딕셔너리, 리스트 등)로 변환
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"파일을 찾을 수 없습니다: {filename}")
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")
    except PermissionError:
        logging.error(f"권한 오류: '{filename}' 파일에 접근할 수 없습니다.")
        raise CustomPermissionError(f"파일에 대한 접근 권한이 없습니다: {filename}")
    except json.JSONDecodeError:
        # JSON 형식이 잘못되었을 경우, 로그를 남기고 사용자 정의 예외를 발생시킴
        logging.error(f"형식 오류: '{filename}' 파일이 올바른 JSON 형식이 아닙니다.")
        raise InvalidFileFormatError(f"파일 형식이 올바르지 않습니다: {filename}")

# CSV 파일 처리 함수
def process_csv_file(filename):
    # CSV 파일을 읽어 리스트의 리스트로 반환
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            return list(reader)
    except FileNotFoundError:
        logging.error(f"파일을 찾을 수 없습니다: {filename}")
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")
    except PermissionError:
        logging.error(f"권한 오류: '{filename}' 파일에 접근할 수 없습니다.")
        raise CustomPermissionError(f"파일에 대한 접근 권한이 없습니다: {filename}")

def process_binary_file(filename):
    # 바이너리 파일을 읽어 바이트(bytes) 객체로 반환
    try:
        # 'rb'는 이진(바이너리) 읽기 모드를 의미
        with open(filename, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"파일을 찾을 수 없습니다: {filename}")
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")
    except PermissionError:
        logging.error(f"권한 오류: '{filename}' 파일에 접근할 수 없습니다.")
        raise CustomPermissionError(f"파일에 대한 접근 권한이 없습니다: {filename}")

def process_file(filename):
    # 파일 확장자에 따라 적절한 처리 함수를 호출
    _, ext = os.path.splitext(filename) # 파일 이름에서 확장자를 분리
    
    if ext.lower() == '.txt':
        return process_text_file(filename)
    elif ext.lower() == '.json':
        return process_json_file(filename)
    elif ext.lower() == '.csv':
        return process_csv_file(filename)
    elif ext.lower() == '.bin':
        return process_binary_file(filename)
    else:
        # 지원하지 않는 파일 형식일 경우 예외 발생
        raise InvalidFileFormatError(f"지원하지 않는 파일 형식입니다: {ext}")

# 메인 실행 함수
def main():
    # 예제 파일을 생성하여 테스트 환경 만들기
    with open("과제 테스트용.txt", "w", encoding="utf-8") as f:
        f.write("이건 과제 테스트용 txt파일입니다.")
    with open("과제 테스트용.json", "w", encoding="utf-8") as f:
        json.dump({"이름": "이태수", "내용": "과제 테스트용 json파일 입니다."}, f)
    with open("과제 테스트용.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name"])
        writer.writerow([1, "이태수"])
    with open("과제 테스트용.bin", "wb") as f:
        f.write(b"This is a binary file for test.")

    logging.info("파일 처리기 실행 시작")
    
    # --- 각종 파일 처리 예제 ---
    try:
        print("\n=== 파일 처리 통합 예제 ===")
        text_content = process_file("과제 테스트용.txt")
        print(f"텍스트 파일 내용: {text_content}")

        json_content = process_file("과제 테스트용.json")
        print(f"JSON 파일 내용: {json_content}")

        csv_content = process_file("과제 테스트용.csv")
        print(f"CSV 파일 내용: {csv_content}")
        
        binary_content = process_file("과제 테스트용.bin")
        print(f"바이너리 파일 내용: {binary_content}")
        
    except FileProcessingError as e:
        print(f"처리 중 오류가 발생했습니다: {e}")
    
    # --- 예외 처리 시뮬레이션 ---
    print("\n\n=== 예외 처리 시뮬레이션 ===")
    
    # FileNotFoundError 발생시키기
    try:
        process_file("nonexistent.txt")
    except FileNotFoundError as e:
        print(f"예외 처리됨: {e}")

    # InvalidFileFormatError 발생시키기
    with open("invalid_format.json", "w") as f:
        f.write("This is not a valid JSON")
    try:
        process_file("invalid_format.json")
    except InvalidFileFormatError as e:
        print(f"예외 처리됨: {e}")
    finally:
        os.remove("invalid_format.json")
        
    # PermissionError 발생시키기 (시스템에 따라 권한 오류가 발생하지 않을 수 있음)
    # 아래 코드는 C:\Windows\System32 같은 시스템 폴더에 파일을 쓰려는 시도를 시뮬레이션
    try:
        if os.name == 'nt': # Windows인 경우
            unwritable_dir = os.path.join(os.environ['WINDIR'], 'System32')
            if os.path.exists(unwritable_dir):
                print("\n=== 권한 오류 시뮬레이션 ===")
                # 존재하지 않는 파일을 열어 쓰기 시도 -> PermissionError 발생 예상
                with open(os.path.join(unwritable_dir, "이상한_파일.txt"), "w") as f:
                    f.write("Test")
    except PermissionError as e:
        print(f"예외 처리됨: {e}")

    logging.info("파일 처리기 실행 완료\n")

    # 예제 파일 정리
    if os.path.exists("과제 테스트용.txt"):
        os.remove("과제 테스트용.txt")
    if os.path.exists("과제 테스트용.json"):
        os.remove("과제 테스트용.json")
    if os.path.exists("과제 테스트용.csv"):
        os.remove("과제 테스트용.csv")
    if os.path.exists("과제 테스트용.bin"):
        os.remove("과제 테스트용.bin")
    
if __name__ == "__main__":
    main()

