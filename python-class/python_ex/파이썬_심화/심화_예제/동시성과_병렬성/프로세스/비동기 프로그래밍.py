import asyncio

async def say_hello(name, delay):
    print(f"{name} 인사 시작")
    await asyncio.sleep(delay)
    print(f"{name} 인사 완료 (대기 시간 : {delay}초)")
    return f"{name}의 결과"

async def main():
    print("프로그램 시작")

    results = await asyncio.gather(
        say_hello("A", 3),
        say_hello("B", 1),
        say_hello("C", 2)
    )

    print(f"모든 결과 : {results}")
    print("프로그램 종료")

if __name__ == "__main__":
    asyncio.run(main())