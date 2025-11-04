import sys

big_list = [i for i in range(10000)]
print(f"리스트  크기 : {sys.getsizeof(big_list)} 바이트")

big_gen = (i for i in range(10000))
print(f"리스트  크기 : {sys.getsizeof(big_gen)} 바이트")



import sys

# 리스트 컴프리헨션
big_list = [i for i in range(10000)]
print(f"리스트  크기 : {sys.getsizeof(big_list)} 바이트")

# 제너레이터 표현식
big_gen = (i for i in range(10000))
print(f"리스트  크기 : {sys.getsizeof(big_gen)} 바이트")