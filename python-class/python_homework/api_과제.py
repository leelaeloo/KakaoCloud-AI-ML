
import requests
import time
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

# API URL
API_URLS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/4",
    "https://jsonplaceholder.typicode.com/posts/5"
]

# 1. 순차 처리
def sequential_processing():
    # URL 리스트를 순차적으로 반복하며 GET 요청을 보냄
    print("--- 1. 순차 처리 시작 ---")
    start_time = time.time()

    for url in API_URLS:
        response = requests.get(url)
        print(f"순차 처리: {url} -> 상태 코드: {response.status_code}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"--- 순차 처리 완료, 소요 시간: {elapsed_time:.4f}초 ---")
    return elapsed_time

# 2. ThreadPoolExecutor 사용
def thread_pool_executor_processing():
    # ThreadPoolExecutor를 사용하여 여러 스레드에서 동시에 GET 요청을 보냄
    print("\n--- 2. ThreadPoolExecutor 사용 시작 ---")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        # map 함수는 각 URL에 대해 requests.get 함수를 실행
        results = executor.map(requests.get, API_URLS)
        
        for url, response in zip(API_URLS, results):
            print(f"스레드 풀: {url} -> 상태 코드: {response.status_code}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"--- ThreadPoolExecutor 완료, 소요 시간: {elapsed_time:.4f}초 ---")
    return elapsed_time

# 3. asyncio와 aiohttp 사용
async def fetch_url(session, url):
    # 비동기적으로 URL에 GET 요청을 보냄
    async with session.get(url) as response:
        print(f"비동기: {url} -> 상태 코드: {response.status}")
        return await response.text()

async def asyncio_processing():
    # asyncio와 aiohttp를 사용하여 비동기적으로 GET 요청을 보냄
    print("\n--- 3. asyncio와 aiohttp 사용 시작 ---")
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in API_URLS]
        await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"--- asyncio/aiohttp 완료, 소요 시간: {elapsed_time:.4f}초 ---")
    return elapsed_time

# 모든 함수를 실행하고 결과를 비교
def main():
    # 메인 함수: 세 가지 처리 방식을 실행하고 결과를 비교
    print("\n동시성과 병렬 처리 성능 비교\n")
    print("-----------------------------------")
    
    # 1. 순차 처리 실행
    sequential_time = sequential_processing()

    print("\n" + "="*50 + "\n")

    # 2. ThreadPoolExecutor 실행
    thread_pool_time = thread_pool_executor_processing()
    
    print("\n" + "="*50 + "\n")

    # 3. asyncio와 aiohttp 실행
    asyncio_time = asyncio.run(asyncio_processing())

    # 결과 요약 및 비교
    print("\n\n=== 최종 성능 비교 ===")
    print(f"순차 처리 소요 시간: {sequential_time:.4f}초")
    print(f"ThreadPoolExecutor 소요 시간: {thread_pool_time:.4f}초")
    print(f"asyncio/aiohttp 소요 시간: {asyncio_time:.4f}초")

    # 가장 빠른 방식 찾기
    min_time = min(sequential_time, thread_pool_time, asyncio_time)
    
    if min_time == sequential_time:
        fastest = "순차 처리"
    elif min_time == thread_pool_time:
        fastest = "ThreadPoolExecutor"
    else:
        fastest = "asyncio/aiohttp"
    
    print(f"\n결론: 가장 빠른 처리 방식은 '{fastest}' 입니다.\n")

if __name__ == "__main__":
    main()

