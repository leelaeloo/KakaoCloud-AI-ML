import numpy as np

# 1차원 배열 인덱싱
arr = np.array([10, 20, 30, 40, 50])
print(arr[0])
print(arr[-1])

# 2차원 배열 인덱싱
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[0, 0])      # 첫 번째 행, 첫 번째 열 : 1
print(arr2d[1, 2])      # 두 번째 행, 세 번째 열 : 6
print(arr2d[2, -1])     # 세 번째 행, 마지막 열 : 9


