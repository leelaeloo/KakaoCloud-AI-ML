# 할 일 리스트 초기화
tasks = []

# 할 일 추가
def add_task(task):
    tasks.append(task)
    print(f"할 일 '{task}'이(가) 추가되었습니다.")

# 할 일 완료 (삭제)
def complete_task(task_index):
    if 0 <= task_index < len(tasks):
        completed = tasks.pop(task_index)
        print(f"할 일 '{completed}'을(를) 완료했습니다!")
    else:
        print("잘못된 할 일 번호입니다.")

# 할 일 목록 보기
def view_tasks():
    if tasks:
        print("\n --- 할 일 목록 ---")
        for i, task in enumerate(tasks):  # task → tasks 수정
            print(f"{i+1}. {task}")
        print("-------------------")
    else:
        print("할 일이 없습니다.")

# 프로그램 실행 예시
add_task("Python 공부하기")
add_task("운동하기")
add_task("책 읽기")
view_tasks()
complete_task(1)  # 주의: 0부터 시작하는 인덱스
view_tasks()