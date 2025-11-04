# 산술 연산자 (기본적인 수학 연산)

a = 20
b = 30
c = 40

# 덧셈 연산자
print(f"덧셈 : {a} + {b} = {a + b}")            # 50

# 뺄셈 연산자
print(f"뺄셈 : {a} - {b} = {a - b}")            # -10

# 곱셈 연산자
print(f"곱셈 : {a} * {b} = {a * b}")            # 600

# 나눗셈 연산자
print(f"나눗셈 : {a} / {b} = {a / b}")          # 0.6666...

# 정수 나눗셈 연산자
print(f"정수 나눗셈 : {a} // {b} = {a // b}")   # 0

# 나머지 연산자
print(f"나머지 : {a} % {b} = {a % b}")          # 20

# 거듭제곱 연산자
print(f"거듭제곱 : {a} ** {b} = {a ** b}")      # 1073741824000...

# 비교 연산자
# 값의 비교와 판단

# 동등 비교 연산자
print(f"{a} == {b} = {a == b}")             # 20 == 30 = False
print(f"{a} == {c} = {a == c}")             # 20 == 40 = False

# 부등 비교 연산자 
print(f"{a} != {b} = {a != b}")             # 20 != 30 = True

# 크다 (>)
print(f"{a} > {b} = {a > b}")               # 20 > 30 = False

# 작다 (<)
print(f"{a} < {b} = {a < b}")               # 20 < 30 = True

# 크거나 같다 (>=)
print(f"{a} >= {b} = {a >= b}")               # 20 >= 30 = False

# 작거나 같다 (<=)
print(f"{a} <= {b} = {a <= b}")               # 20 <= 30 = True

# 문자열 비교 (알파벳 순)
str1 = "banana"
str2 = "pineapple"
print(f"'{str1}' < '{str2}' = {str1 < str2}")       # 'banana' < 'pineapple' = True

# 다른 타입 비교
print(f"4 == '4' = {4 == '4'}")                     # 4 == '4' = False
print(f"4 == int('4') = {4 == int('4')}")           # 4 == int('4') = True


