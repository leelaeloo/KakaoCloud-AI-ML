# 집합 생성

# 1. 중괄호로 생성
foods = {"짜장면", "탕수육", "짬뽕"}

# 2. set() 함수 사용
numbers = set([11, 22, 33, 22, 11])
print(numbers)      # {33, 11, 22}

# 3. 문자열로 생성 (각 문자가 요소가 됨)
char = set("Lee Tae Soo")
print(char)         # {'a', ' ', 'o', 'L', 'S', 'e', 'T'}

# 4. 빈 집합 생성 (주의 : 빈 중괄호 {}는 딕셔너리)
empty_set = set()   # 빈 집합
not_set = {}        # 빈 딕셔너리, 집합 아님

# 5. 집합 컴프리헨션
squares = {x**2 for x in range(1, 8)}
print(squares)      # {1, 4, 36, 9, 16, 49, 25}