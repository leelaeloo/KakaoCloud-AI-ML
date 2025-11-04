# 튜플 사용 케이스_3
# 네임드 튜플 활용
# 구조체처럼 필드명으로 접근 가능한 튜플이 필요할 때 유용

from collections import namedtuple

# 네임드 튜플 정의
Person = namedtuple('Person', ['name', 'age', 'city'])

# 생성 및 사용
person1 = Person('이태수', 25, '인천')

# 인덱스로 접근
print(person1[0]) # 이태수

# 필드명으로 접근 (가독성 높음)
print(person1.name) # 이태수
print(person1.age) # 25
print(person1.city) # 인천