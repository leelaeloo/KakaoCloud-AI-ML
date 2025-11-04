import numpy as np


# Numpy 배열(ndarray) 기초

# 1차 원 배열
arr1 = np.array([1, 2, 3, 4, 5])
print(arr1)

# 2차월 배열 (행렬)
arr2 = np.array([[1, 2, 3], [4, 5, 6]])
print(arr2)


# 0으로 채워진 배열
zeros = np.zeros((3, 4))        # 3행 4열의 0 행렬
print(zeros)

# 1로 채워진 배열
ones = np.ones((2, 3))          # 2행 3열의 1 행렬
print(ones)

# 특정 범위의 균일한 간격 배열
range_arr = np.arange(0, 12, 2)
print(range_arr)

# 선행 간격 배열
linear_space = np.linspace(0, 1, 5)
print(linear_space)

# 랜덤 배열
random_arr = np.random.random((2, 2))
print(random_arr)

arr = np.array([[1, 2, 3], [4, 5, 6]])

print(f"배열 차원 : {arr.ndim}")
print(f"배열 형태 : {arr.shape}")
print(f"배열 크기 : {arr.size}")
print(f"요소 데이터 타입 : {arr.dtype}")
print(f"각 요소 바이트 크기: {arr.itemsize}")
print(f"전체 배열 바이트 크기 : {arr.nbytes}")

# 전치 (행과 열 바꾸기)
print("원본 배열 : ")
print(arr)
print("전치 배열 (T) : ")
print(arr.T)                    #[[1 4], [2 5], [3 6]]

# 배열 형태 변경 (reshape)
arr1d = np.arange(12)
arr2d = arr1d.reshape(3, 4)
print("reshape 결과 : ")
print(arr2d)

# 배열 평탄화 (1차원으로 변환)
print("평탄화 결과 (flatten) : ")
print(arr2d.flatten())          # [0 1 2 3 4 5 6 7 8 9 10 11]

# 데이터 타입 변환
arr_float = arr.astype(np.float64)
print(f"타입 변환 후 : {arr_float.dtype}")

# 통계 메서드
data = np.array([1, 2, 3, 4, 5])
print(f"합계 : {data.sum()}")           # 15
print(f"평균 : {data.mean()}")          # 3.0
print(f"최소값 : {data.min()}")         # 1
print(f"최대값 : {data.max()}")         # 5
print(f"표준편차 : {data.std()}")       # 1.4142
print(f"분산 : {data.var()}")           # 2.0
print(f"누적합 : {data.cumsum()}")      # [1 3 6 10 15]

# 조건 기반 인덱싱
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
print("짝수 요소만 선택 : ")
print(arr[arr % 2 == 0])        # [2 4 6 8]

# 배열 연산 메서드
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print("행렬 곱셈 (dot) : ")
print(a.dot(b))                 # [[19 22], [43 50]]

# 요소별 곱셈
element_wise = a * b
print(element_wise)
