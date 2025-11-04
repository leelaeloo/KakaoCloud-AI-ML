import threading
import time

data = None
condition = threading.Condition()

def wait_for_data():
    print("\n대기 스레드 : 데이터를 기다립니다 ...\n")

    with condition:
        condition.wait()
        print(f"\n대기 스레드 : 데이터 {data}를 받았습니다.\n")

def prepare_data():
    global data

    print("\n준비 스레드 : 데이터 준비 중 ...\n")
    time.sleep(2)

    with condition:
        data = "준비된 데이터"
        print("\n준비 스레드 : 데이터가 준비되었습니다.\n")
        condition.notify()

t1 = threading.Thread(target=wait_for_data)
t2 = threading.Thread(target=prepare_data)

t1.start()
t2.start()

t1.join()
t2.join()