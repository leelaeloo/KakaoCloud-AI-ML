
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# 테스트 웹사이트
URLS = [
    'https://www.naver.com',
    'https://www.google.com',
    'https://www.youtube.com',
    'https://www.facebook.com',
    'https://www.instagram.com',
    'https://www.wikipedia.org',
]

# --- 순차 처리 함수 ---
def sequential_download():
    # URL 리스트를 순차적으로 접근합
    print("\n--- 순차 처리 시작 ---")
    start_time = time.time()
    
    # URL 리스트를 순서대로 반복하며 한 번에 하나의 요청을 처리
    for url in URLS:
        try:
            # requests.get() 함수는 응답을 받을 때까지 기다림
            requests.get(url, timeout=5)
            print(f"순차 처리: {url} -> 성공")
        except requests.exceptions.RequestException as e:
            # requests.exceptions.RequestException는 requests 라이브러리에서 발생하는 모든 네트워크 관련 오류를 처리
            # 웹 연결 실패, 타임아웃 등 다양한 예외를 포괄하며, 프로그램이 중단되지 않고 다음 작업을 이어갈 수 있게 함
            print(f"순차 처리: {url} -> 실패 ({e})")
            
    end_time = time.time()
    print(f"--- 순차 처리 완료, 소요 시간: {end_time - start_time:.2f}초 ---\n")

# --- 스레드풀을 사용한 병렬 처리 함수 ---
def download_url(url):
    try:
        response = requests.get(url, timeout=5)
        return url, "성공"
    except requests.exceptions.RequestException as e:
        return url, f"실패 ({e})"

def thread_pool_download():
    # ThreadPoolExecutor를 사용하여 URL에 병렬적으로 접근
    # 여러 스레드가 동시에 요청을 보내기 때문에 순차 처리보다 훨씬 빠름
    print("--- 스레드풀 처리 시작 ---")
    start_time = time.time()
    
    # with 문을 사용하여 스레드풀을 생성하고, 작업 완료 후 자동으로 종료
    # max_workers=5는 풀 안에 최대 5개의 스레드를 미리 생성해 놓겠다는 의미
    with ThreadPoolExecutor(max_workers=5) as executor:
        # executor.map() 함수는 URLS 리스트의 각 항목을 download_url 함수에 전달
        # 풀에 있는 스레드들이 작업을 나누어 처리하며, 모든 작업이 완료될 때까지 기다림
        results = executor.map(download_url, URLS)
        
        # results는 모든 작업의 결과가 담긴 이터레이터
        for url, status in results:
            print(f"스레드풀 처리: {url} -> {status}")
            
    end_time = time.time()
    print(f"--- 스레드풀 처리 완료, 소요 시간: {end_time - start_time:.2f}초 ---\n")

# --- 메인 실행 부분 ---
if __name__ == "__main__":
    # 순차 처리를 실행하여 기준 성능을 측정
    sequential_download()
    
    # 스레드풀을 사용한 병렬 처리를 실행하여 성능을 비교
    thread_pool_download()

