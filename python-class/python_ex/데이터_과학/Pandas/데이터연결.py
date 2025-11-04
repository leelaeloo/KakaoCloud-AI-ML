# 데이터 연결
import pandas as pd

# 데이터프레임 2개 생성
df1 = pd.DataFrame({
    'A' : ['A0', 'A1', 'A2'],
    'B' : ['B0', 'B1', 'B2']
})

df2 = pd.DataFrame({
    'A' : ['A3', 'A4', 'A5'],
    'B' : ['B3', 'B4', 'B5']
})

print("DataFrame 1 : ")
print(df1)
print("\nDataFrame 2 : ")
print(df2)

# 세로 방향으로 연결(행 추가)
result_rows = pd.concat([df1, df2])
print("\n세로 연결(행 추가) : ")

# 가로 방향으로 연결(열 추가)
df3 = pd.DataFrame({
    'C' : ['C0', 'C1', 'C2'],
    'D' : ['D0', 'D1', 'D2']
})

result_cols = pd.concat([df1, df3], axis=1)
print("\n가로 연결(열 추가) : ")
print(result_cols)