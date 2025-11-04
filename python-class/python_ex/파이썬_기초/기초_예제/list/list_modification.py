foods = ["치킨", "피자", "햄버거"]

# 요소 변경
foods[1] = "짜장면"      # ['치킨', '짜장면', '햄버거']
print(foods)

# 요소 추가
foods.append("삼겹살")   # ['치킨', '짜장면', '햄버거', '삼겹살']
print(foods)

# 특정 위치에 삽임
foods.insert(1, "만두")  # ['치킨', '만두', '짜장면', '햄버거', '삼겹살']
print(foods)

# 리스트 확장
more_food = ["탕수육", "짬뽕"]      # ['치킨', '만두', '짜장면', '햄버거', '삼겹살', '탕수육', '짬뽕']
foods.extend(more_food)
print(foods)

# 요소 제거 
foods.remove("햄버거")               # ['치킨', '만두', '짜장면', '삼겹살', '탕수육', '짬뽕']
print(foods)

# 특정 위치 요소 제거 및 반환
removed = foods.pop(2)               # '짜장면' 제거 및 반환 -> ['치킨', '만두', '삼겹살', '탕수육', '짬뽕']
print(removed)
print(foods)

# 리스트 정렬
foods.sort()                         # ['만두', '삼겹살', '짬뽕', '치킨', '탕수육'] (알파벳 순)
print(foods)

# 리스트 역순
foods.reverse()
print(foods)                         # ['탕수육', '치킨', '짬뽕', '삼겹살', '만두']

# 리스트 길이
print(len(foods))                    # 5

# 요소 개수 세기
foods.append("삼겹살")              # 2
print(foods.count("삼겹살"))        

# 요소 위치 찾기
print(foods.index("탕수육"))        # 0

# 리스트 내용 비우기
foods.clear()                       # []
print(foods)
