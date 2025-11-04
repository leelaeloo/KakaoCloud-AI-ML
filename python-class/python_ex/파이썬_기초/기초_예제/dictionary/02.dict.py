# 딕셔너리 컴프리헨션
# 1. 기본 형태
squares = {x: x**2 for x in range(1, 8)}               
print(squares)      # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49}

# 2. 조건부 딕셔너리와 컴프리헨션
even_squares = {x: x**2 for x in range(1, 14) if x % 2 == 0}
print(even_squares) # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100, 12: 144}

# 3. 값 변환 예제
foods = ["햄버거", "치킨", "피자"]
food_lenghts = {food: len(food) for food in foods}
print(food_lenghts) # {'햄버거': 3, '치킨': 2, '피자': 2}