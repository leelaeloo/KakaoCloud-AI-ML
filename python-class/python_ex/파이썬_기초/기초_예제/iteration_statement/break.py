# break
# 반복문을 즉시 종료하고 다음 코드로 넘어감

# 1. 특정 값 찾기
numbers = [1, 2, 3, 4, 5, 6, 7]
search_for = 5

for num in numbers:
    print(f"현재 확인 중: {num}")
    if num == search_for:
        print(f"{search_for}을(를) 찾았습니다!")
        break
print("검색 완료")

# 2. 사용자 입력으로 반복 제어
while True:
    response = input("계속하시겠습니까? (y/n): ")
    if response.lower() == 'n':
        print("프로그램을 종료합니다.")
        break
    print("계속 진행합니다.")