
import asyncio
import aiohttp
import time

websites = [
    "https://www.google.com",
    "https://www.naver.com",
    "https://www.daum.net",
    "https://www.github.com",
    "https://www.python.org",
    "https://www.microsoft.com",
    "https://www.amazon.com",
    "https://www.reddit.com"
]

# --- 단일 웹 요청 함수 ---
async def fetch(session, url):
    # aiohttp를 사용하여 비동기적으로 URL에 GET 요청을 보냄
    # :param session: aiohttp.ClientSession 객체. 요청을 보낼 때 사용
    print(f"{url} 요청 시작")
    try:
        start_time = time.time()
        # aiohttp.ClientSession.get()은 비동기 작업으로, 응답을 기다리는 동안
        # asyncio가 다른 작업을 처리할 수 있도록 제어권을 넘김
        # async with 문을 사용하여 세션 관리를 자동으로 처리
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            # await response.text()는 응답 본문을 모두 읽을 때까지 기다림
            content = await response.text()
            elapsed = time.time() - start_time
            print(f"{url} 응답 완료 : {len(content)} 바이트 (소요시간 : {elapsed:.2f}초)")
            # 작업이 완료되면 URL, 응답 데이터 크기, 소요 시간을 반환
            return url, len(content), elapsed
    except Exception as e:
        print(f"{url} 오류 발생 : {e}")
        return url, 0, 0
        
# --- 순차 처리 함수 ---
async def fetch_all_sequential(urls):
    """
    URL 리스트를 순차적으로(하나씩) 비동기 요청합니다.
    """
    print("\n --- 순차 처리 --- ")
    start_time = time.time()
    results = []
    # aiohttp.ClientSession 객체를 생성
    async with aiohttp.ClientSession() as session:
        # for 루프를 사용하여 URL을 순서대로 반복
        for url in urls:
            # await 키워드가 붙었기 때문에, fetch 함수가 완료될 때까지 기다림
            # 다음 URL은 이전 URL의 요청이 완전히 끝난 후에야 시작됨
            result = await fetch(session, url)
            results.append(result)

    end_time = time.time()
    print(f"순차 처리 완료 : {end_time - start_time:.2f}초 소요")
    return results

# --- 병렬 처리 함수 ---
async def fetch_all_parallel(urls):
    # URL 리스트를 병렬적으로(동시에) 비동기 요청합니다.
    print("\n --- 병렬 처리 --- ")
    start_time = time.time()
    results = []
    async with aiohttp.ClientSession() as session:
        # fetch 함수를 호출하여 각 URL에 대한 코루틴 객체를 생성
        # 이 시점에는 실제 요청이 보내지지 않고, 작업 목록만 만들어짐
        tasks = [fetch(session, url) for url in urls]
        
        # asyncio.gather()는 tasks 리스트의 모든 코루틴이 완료될 때까지 기다림
        # asyncio의 이벤트 루프가 이 작업들을 동시에 실행하도록 스케줄링함
        results = await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"병렬 처리 완료 : {end_time - start_time:.2f}초 소요")
    return results

# --- 메인 실행 함수 ---
async def main():
    # 순차 처리와 병렬 처리 함수를 각각 실행하고 결과를 비교
    # 순차 처리를 실행
    sequential_results = await fetch_all_sequential(websites)
    # 두 실행 결과를 섞이지 않게 하기 위해 잠시 기다림
    await asyncio.sleep(1)
    # 병렬 처리를 실행
    parallel_results = await fetch_all_parallel(websites)

    print("\n --- 결과 요약 --- ")
    # 처리된 바이트 합산을 통해 작업 성공 여부를 간접적으로 확인
    seq_total_bytes = sum(r[1] for r in sequential_results)
    par_total_bytes = sum(r[1] for r in parallel_results)

    print(f"순차 처리 : 총 {seq_total_bytes} 바이트")
    print(f"병렬 처리 : 총 {par_total_bytes} 바이트\n")
    
if __name__ == "__main__":
    # asyncio.run() 함수는 최상위 비동기 함수(main)를 실행하고 이벤트 루프를 시작
    asyncio.run(main())


