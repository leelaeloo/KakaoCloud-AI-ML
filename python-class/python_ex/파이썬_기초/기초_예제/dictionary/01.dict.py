import time

# 데이터 준비
data_size = 1000000  # 백만 개의 데이터
search_key = f"key_{data_size-1}" # 마지막 요소 검색 (최악의 경우)

# 딕셔너리 생성
dict_data = {f"key_{i}": i for i in range(data_size)}

# 리스트 생성
list_data = [(f"key_{i}", i) for i in range(data_size)]

# 딕셔너리 검색 (O(1)) 시간 측정
start_time = time.time()
result_dict = dict_data[search_key]
dict_time = time.time() - start_time
print(f"\n딕셔너리 검색 시간: {dict_time:.6f}초\n")     # 딕셔너리 검색 시간 : 0.000014초
print(f"\n찾은 값: {result_dict}\n")                    # 찾은 값 : 999999