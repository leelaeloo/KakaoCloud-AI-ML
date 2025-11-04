import multiprocessing
import time

def add_to_shared(shaed_value, Lock, increment):
    for _ in range(5):
        with Lock:
            shaed_value.value += increment
        time.sleep(0.1)

    print(f"프로세스 {multiprocessing.current_process().name}: 작업 완료")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=count_up, args=("A", 5))
    p2 = multiprocessing.Process(target=count_up, args=("B", 3))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("모든 프로세스 종료")
