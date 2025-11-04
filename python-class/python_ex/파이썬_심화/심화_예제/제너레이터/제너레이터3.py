# 센서 -> 서버에 데이터를 계속 보냄
import time
import random

def sensor_data_stream():
    while True:
        temperature = 20 + random.uniform(-5, 5)
        yield f"온도 {temperature:.2f}C, 시간 : {time.strftime('%H, %M, %S')}"
        time.sleep(1)


stream = sensor_data_stream()
for _ in range(5):
    print(next(stream))