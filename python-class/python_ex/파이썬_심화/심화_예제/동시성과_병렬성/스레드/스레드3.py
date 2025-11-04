import threading
import time

counter = 0
counter_lock = threading.Lock() # 락 객체 생성

def increment_with_lock(count):
    global counter
    for _ in range(count):
        counter_lock.acquire() # 락 획득
        try:
            current = counter
            time.sleep(0.001)
            counter = current + 1
        finally:
            counter_lock.release() # 락 해제

# 두 개의 스레드 생성
t1 = threading.Thread(target=increment_with_lock, args=(1000,))
t2 = threading.Thread(target=increment_with_lock, args=(1000,))

t1.start()
t2.start()

t1.join()
t2.join()

print(f"락 사용 후 최종 카운터 값: {counter}") # 항상 2000