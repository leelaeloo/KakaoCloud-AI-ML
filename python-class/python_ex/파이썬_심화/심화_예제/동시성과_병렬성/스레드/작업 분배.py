import threading
import queue
import time
import random

# # --- 작업 및 결과 큐 초기화 ---
# task_queue : 작업을 담아 워커 스레드에게 전달
task_queue = queue.Queue()
# result_queue : 워커 스레드가 처리한 결과를 담아 수집기에게 전달
result_queue = queue.Queue()

# 생산자 역할
def create_tasks():
    print("\n작업 생성 시작")
    # 10개의 가상 직업 생성
    for i in range(10):
        task = f"작업{-1}"
        # task_queue에 작업 추가(큐가 가득 차면 공간이 생길 때까지 대기)
        task_queue.put(task)
        print(f"작업 추가 : {task}")
        # 작업 생성 간에 무작위 시간 간격 두기
        time.sleep(random.uniform(0.1, 0.3))

    # 워커 스레드 수만큼 종료 신호(None)를 큐에 추가
    # 워커 스레드 3개가 모두 None을 받고 종료
    for _ in range(3):
        task_queue.put(None)
    print("모든 작업 생성 완료")

# 소비자 역할
def worker(worker_id):
    print(f"워커 {worker_id} 시작")
    while True:
        # task_queue에서 작업 가져오기(큐가 비어있으면 작업이 들어올 때까지 대기)
        task = task_queue.get()
        # 종료 신호(None)을 받으면 무한 루프 탈출 후 스레드 종료
        if task is None:
            print(f"워커 {worker_id} 종료")
            break

        print(f"워커 {worker_id}가 {task} 처리 중 ...")
        processing_time = random.uniform(0.5, 1.5)
        time.sleep(processing_time)

        result = f"{task} 완료 (소요시간 : {processing_time:.2f}초)"
        # 처리 결과를 result_queue에 추가
        result_queue.put((worker_id, result))

        # 현재 작업을 완료했음을 큐에 알림
        task_queue.task_done()
        print(f"남은 작업 수 : {task_queue.qsize()}")

# 수집기 역할
def result_collector():
    print("\n결과 수집 시작\n")
    results = []

    # 모든 결과(10개)가 수집될 때까지 반복
    # 워커 스레드들은 task_queue에서 None을 받고 종료되지만,
    # result_collector는 task_queue와 직접 연결되어있지 않으므로,
    # 총 작업 수(10개)를 기반으로 반복
    for _ in range(10):
        # result_queue에서 결과 가져오기(큐가 비어있으면 대기)
        worker_id, result = result_queue.get()
        print(f"결과 수신 : 워커 {worker_id} -> {result}")
        results.append(result)
        # 현재 결과 수집을 완료 했다고 큐에 알림
        result_queue.task_done()

        print(f"\n총 {len(results)}개 결과 수집 완료\n")

# --- 스레드 생성 및 실행 ---

# 작업 생성 스레드
creator = threading.Thread(target=create_tasks)
# 작업을 처리하는 워커 스레드 3개 생성(arg를 통해 워커 ID 전달)
workers = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
# 결과를 수집하는 스레드
collector = threading.Thread(target=result_collector)

# 모든 스레드 시작
creator.start()
for w in workers:
    w.start()
collector.start()

# --- 메인 스레드가 모든 서브 스레드가 종료될 때 까지 대기 ---
# join()을 호출하여 해당 스레드가 종료될 때까지 기다림
creator.join()
for w in workers:
    w.join()
collector.join()

print("\n모든 작업 완료\n")

