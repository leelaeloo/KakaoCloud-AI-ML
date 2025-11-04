# 튜플 사용 케이스_4
# 튜플의 불변성은 함수형 프로그래밍 스타일에 적합
def add_to_each(data, value):
    # 원본 데이터를 변경하지 않고 새 튜플 반환
    return tuple(item + value for item in data)

numbers = (5, 6, 7)
new_numbers = add_to_each(numbers, 10)      # add_to_each 함수를 호출하여 numbers 튜플에 10을 더함

print(numbers)       # (5, 6, 7) - 원본 그대로 유지
print(new_numbers)   # (15, 16, 17) - 새 튜플 생성