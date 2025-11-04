import numpy as np
import matplotlib.pyplot as plt
import time

# 삼각함수로 시계 만들기
def create_clock():
    # 현재 시간 가져오기
    current_time = time.localtime()
    hour = current_time.tm_hour % 12
    minute = current_time.tm_min
    second = current_time.tm_sec

    # 각도를 라디안으로 변환
    # Matplotlib의 y축이 위로 향하기 때문에 np.pi/2 (90도)를 더해 12시를 0도로 설정
    hour_angle = -2 * np.pi * (hour + minute/60) / 12 + np.pi/2
    minute_angle = -2 * np.pi * minute / 60 + np.pi/2
    second_angle = -2 * np.pi * second / 60 + np.pi/2

    # 시계 바늘의 x, y 좌표 계산
    hour_x = 0.5 * np.cos(hour_angle)
    hour_y = 0.5 * np.sin(hour_angle)

    minute_x = 0.8 * np.cos(minute_angle)
    minute_y = 0.8 * np.sin(minute_angle)

    second_x = 0.9 * np.cos(second_angle)
    second_y = 0.9 * np.sin(second_angle)

    # 한글 폰트 설정
    plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
    fig, ax = plt.subplots(figsize=(8, 8))

    # 시계 원 그리기
    circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
    ax.add_patch(circle)

    # 시계 숫자 그리기
    for hour_num, angle in [(12, np.pi/2), (3, 0), (6, -np.pi/2), (9, np.pi)]:
        x = 1.1 * np.cos(angle)
        y = 1.1 * np.sin(angle)
        ax.text(x, y, str(hour_num), ha='center', va='center', fontsize=14, fontweight='bold')

    # 시계 바늘 그리기 (반복문 밖으로 이동)
    ax.plot([0, hour_x], [0, hour_y], 'b-', linewidth=6, label=f'시침 ({hour}시)')
    ax.plot([0, minute_x], [0, minute_y], 'g-', linewidth=3, label=f'분침 ({minute}분)')
    ax.plot([0, second_x], [0, second_y], 'r-', linewidth=1, label=f'초침 ({second}초)')

    # 시계 중심점 그리기
    ax.plot(0, 0, 'ko', markersize=8)

    # 축 범위, 비율 및 제목 설정
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.set_title(f'삼각함수 시계\n현재 시간: {hour:02d}:{minute:02d}:{second:02d}', fontsize=16)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.axis('off') # 축 제거

    # 그래프 보여주기 (반복문 밖으로 이동)
    plt.show()

if __name__ == '__main__':
    create_clock()
