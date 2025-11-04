
# 청소 로봇 춘식이😾
class Choonsic:
    def __init__(self, name, model):
        self.name = name                 # 로봇 이름
        self.model = model               # 로봇의 모델병
        self.is_cleaning = False         # 현재 청소 중인지
        self.battery_level = 80          # 초기 배터리 레벨

    # 춘식이 청소 시작
    def start_cleaning(self):
        if self.is_cleaning:
            print(f"\n이미 청소 중입니다.\n")
            return

        print(f"\n춘식이😾가 청소를 시작합니다.")
        self.is_cleaning = True

    # 춘식이 청소 중단
    def stop_cleaning(self):
        if not self.is_cleaning:
            print(f"\n춘식이😾는 현재 멈춰 있습니다.\n")
            return

        print(f"\n춘식이😾가 청소를 중단합니다.")
        self.is_cleaning = False

    # 춘식이 베터리
    def charge(self, duration):
        charge_amount = duration * 2  # 1분당 2% 충전
        self.battery_level += charge_amount

        # 배터리 레벨이 100%를 초과하지 않도록 제한
        if self.battery_level > 100:
            self.battery_level = 100
        
        print(f"\n춘식이😾가 {duration}분 동안 충전했습니다. 현재 배터리: {self.battery_level}%")

    def report_status(self):
        status_message = "\n춘식이😾가 청소중입니다" if self.is_cleaning else "대기 중"
        return f"\n춘식이😾 (모델: {self.model}) - 현재 상태: {status_message}, 배터리: {self.battery_level}%\n"

# 작업 클래스
class Task:
    def __init__(self, description, duration):
        self.description = description       # 작업에 대한 설명
        self.duration = duration             # 작업 소요 시간
        self.is_completed = False            # 작업 완료 여부

    # 작업을 완료 상태로 변경
    def complete(self):
        self.is_completed = True
        print(f"작업 '{self.description}' 완료.")

# Choonsik 객체 생성
my_choonsic = Choonsic("춘식", "Choon sik - Clean Bot 01")
print(my_choonsic.report_status())

# Task 객체 생성
cleaning_task = Task("거실 바닥 청소", 30)

# 춘식이 작업 시작
my_choonsic.start_cleaning()
print(my_choonsic.report_status())

# 춘식이 완료
my_choonsic.battery_level -= cleaning_task.duration * 0.5 
print(f"{cleaning_task.duration}분 동안 청소 후 배터리 소모: {my_choonsic.battery_level}%")
cleaning_task.complete()

# 춘식이 작업 멈춤
my_choonsic.stop_cleaning()
print(my_choonsic.report_status())

# 춘식이 충전
my_choonsic.charge(15)
print(my_choonsic.report_status())

# 추가적인 충전 테스트
my_choonsic.charge(20) # 배터리가 100%를 초과하지 않도록 확인
print(my_choonsic.report_status())

