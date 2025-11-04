import multiprocessing
import time
import os

# 각 프로세스가 실행할 작업 함수
def process_task(task_id):
    # CPU 연산이 많이 필요한 가상 작업을 수행
    # task_id: 현재 작업의 고유 ID
    # 반환값: (task_id, 결과, 프로세스 ID) 튜플
    # 현재 실행 중인 프로세스의 고유 ID를 가져옴
    process_id = os.getpid()
    print(f"작업 {task_id} 시작 (프로세스 ID: {process_id})")
    
    # 1000만 번의 덧셈 연산을 수행하여 CPU를 많이 사용하도록 시뮬레이션 실행
    result = 0
    for i in range(10000000):
        result += 1
    
    print(f"작업 {task_id} 완료 (프로세스 ID: {process_id})")
    return task_id, result, process_id

# 스크립트가 직접 실행될 때만 아래 코드가 동작
# Windows 운영체제에서 multiprocessing을 사용할 때 필수
if __name__ == "__main__":
    # 시스템의 CPU 코어 수를 확인하여 프로세스 풀의 크기를 결정
    num_cores = multiprocessing.cpu_count()
    print(f"시스템 CPU 코어 수: {num_cores}")

    # 총 10개의 작업을 정의
    tasks = range(10)

    # --- 순차 처리(Sequential Processing) 시작 ---
    print("\n=== 순차 처리 시작 ===")
    start_time = time.time()
    
    # 리스트 컴프리헨션을 사용해 모든 작업을 순서대로 처리
    sequential_results = [process_task(i) for i in tasks]
    
    end_time = time.time()
    print(f"순차 처리 시간: {end_time - start_time:.2f}초")
    
    # --- 병렬 처리(Parallel Processing) 시작 ---
    print("\n=== 병렬 처리 시작 ===")
    start_time = time.time()
    
    # with 문을 사용하여 프로세스 풀을 생성하고, 작업 완료 후 자동으로 정리
    # processes=num_cores를 통해 시스템 코어 수만큼의 프로세스를 풀에 생성
    with multiprocessing.Pool(processes=num_cores) as pool:
        # pool.map() 함수는 tasks 리스트의 각 항목을 process_task 함수의 인수로 전달하여
        # 풀에 있는 여러 프로세스에 분배
        # 모든 작업이 완료되면 결과 리스트를 반환
        parallel_results = pool.map(process_task, tasks)
        
    end_time = time.time()
    print(f"병렬 처리 시간: {end_time - start_time:.2f}초")

    # --- 결과 분석 및 출력 ---
    print("\n=== 결과 분석 ===")
    # 병렬 처리 시 사용된 고유한 프로세스 ID를 확인
    # 이를 통해 여러 프로세스가 실제로 사용되었음을 알 수 있음
    process_ids = set(result[2] for result in parallel_results)
    print(f"사용된 프로세스 수: {len(process_ids)}")
    print(f"프로세스 ID 목록: {process_ids}")

