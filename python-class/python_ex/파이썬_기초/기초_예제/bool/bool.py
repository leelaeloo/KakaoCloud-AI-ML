# 비교 연산
equal = (5 == 5)        # True
print(equal)

not_equal = (5 != 3)    # Ture
print(not_equal)

greater = (5 > 3)       # True
print(greater)

less = ( 5 < 3)         # False
print(less)

# 복합 비교 연산
x = 10
complex_check = (5 < x < 15)        # True (5 < 10 and 10 < 15)
print(complex_check)

# 객체 비교
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = list1

print(list1 == list2)       # Ture
print(list1 is list2)       # False
print(list1 is list3)       # True