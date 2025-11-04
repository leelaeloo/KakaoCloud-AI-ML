import threading
import time

def background_task():
    while True:
        print("\n백그라운드 작업 실행 중 ...\n")
        time.sleep(1)

# 데몬 스레드 실행
daemon_thread = threading.Thread(target=background_task, daemon=True)
daemon_thread.start()

# 메인 스레드는 3초 후 종료
print("\n메인 스레드 작업 중 ...\n")
time.sleep(1)
print("\n메인 스레드 종료\n")
# 마지막 print 출력 후 스레드 종료