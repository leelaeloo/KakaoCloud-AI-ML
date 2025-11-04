# 튜플 사용 케이스_2

# 성능과 메모리 효율성
import sys

my_list = [10, 20, 30, 40, 50]
my_tuple = (1, 2, 3, 4, 5)

# 메모리 사용량 비교
print(f"리스트 크기 : {sys.getsizeof(my_list)} 바이트")         # 리스트 크기 : 104 바이트
print(f"튜플 크기 : {sys.getsizeof(my_tuple)} 바이트")          # 튜플 크기 : 80 바이트

# 성능 비교
import timeit

list_time = timeit.timeit(stmt="[1, 2, 3, 4, 5]", number=1000000)       
tuple_time = timeit.timeit(stmt="(1, 2, 3, 4, 5)", number=1000000)

print(f"리스트 생성 시간 : {list_time:.6f}초")                   # # 리스트 생성 시간 : 0.088134초
print(f"튜플 생성 시간 : {tuple_time:.6f}초")                    # 튜플 생성 시간 : 0.014007초


