import threading
import time

event = threading.Event()

def waiter():
    print("\n대기자 : 이벤드 기다리는 중 ...\n")
    event.wait()
    print("\n대기자 : 이벤트를 수신하고 작업 진행\n")

def setter():
    print("\n설정자 : 작업 중 ...\n")
    time.sleep(3)
    print("\n설정자 : 이제 이벤트를 설정합니다.\n")
    event.set()

t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=setter)

t1.start()
t2.start()