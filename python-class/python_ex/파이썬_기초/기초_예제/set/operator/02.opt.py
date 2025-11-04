# 멤버십 연산자
# 리스트에서의 활용

food = ["피자", "치킨", "파스타", "샐러드"]
print(f"'치킨' in food: {'치킨' in food}") # 결과: True
print(f"'김치' in food: {'김치' in food}") # 결과: False
print(f"'김치' not in food: {'김치' not in food}") # 결과: True

# 문자열에서의 활용 (부분 문자열 검색)
message = "맛있는 저녁 메뉴!"
print(f"'저녁' in message: {'저녁' in message}") # 결과: True
print(f"'아침' in message: {'아침' in message}") # 결과: False

# 튜플에서의 활용
numbers = (10, 20, 30, 40, 50)
print(f"30 in numbers: {30 in numbers}") # 결과: True
print(f"70 not in numbers: {70 not in numbers}") # 결과: True

# 논리 연산자
# 조건의 조합

# 논리 연산자 예시
a = False
b = True
c = True

# and 연산자 (두 조건 모두 참일 때만 참)
print(f"'{a}' and '{b}' = {a and b}") # 결과: False
print(f"'{a}' and '{c}' = {a and c}") # 결과: False

# or 연산자 (두 조건 중 하나라도 참이면 참)
print(f"'{a}' or '{b}' = {a or b}") # 결과: True
print(f"'{b}' or '{b}' = {b or b}") # 결과: True

# not 연산자 (조건의 결과를 반대로)
print(f"not '{a}' = {not a}") # 결과: True
print(f"not '{b}' = {not b}") # 결과: False

# 복합 논리 연산
print(f"'{a}' and '{b}' or '{c}' = {a and b or c}") # 결과: True
print(f"'{a}' and ('{b}' or '{c}') = {a and (b or c)}") # 결과: False

# 할당 연산자
# 변수에 값 할당하기

# 문자열에 대한 복합 할당 연산자
message = "안녕하세요"
message += " 반갑습니다" # message = message + " 반갑습니다"와 동일
print(f"message += ' 반갑습니다' → message = {message}") # 결과: 안녕하세요 반갑습니다

# 다중 할당
a, b, c = 10, 20, 30
print(f"a, b, c = 10, 20, 30 → a={a}, b={b}, c={c}") # 결과: a=10, b=20, c=30

# 값 교환 (swap)
x, y = 50, 100
print(f"교환 전: x={x}, y={y}")
x, y = y, x
print(f"교환 후: x={x}, y={y}") # 결과: x=100, y=50