
import pandas as pd
import numpy as np

# 결측치(Missing Values) 처리
df = pd.DataFrame({
    'A' : [1, 2, np.nan, 4, 5],
    'B' : [np.nan, 2, 3, 4, 5],
    'C' : [1, 2, 3, np.nan, np.nan]
})
print("\n원본 데이터 : ")
print(df)

# 결측치 확인
print("\n결측치 여부 : ")
print(df.isna())

# 결측치 개수 확인
print("\n열별 개측치 개수 : ")
print(df.isna().sum())

# 결측치 처리 방법 1 : 삭제
df_dropped = df.dropna()        # 결측치가 있는 행 모두 삭제
print("\n결측치 행 삭제 후 : ")
print(df_dropped)

# 결측치 처리 방법 2 : 채우기
df_filled = df.fillna(0)        # 결측치를 0으로 채우기
print("\n결측치를 0으로 채운 후 : ")
print(df_filled)

# 결측치 처리 방법 3 : 열별 평균으로 채우기
df_mean = df.fillna(df.mean())  # 각 열의 평균값으로 채우기
print("\n결측치를 평균으로  채운 후 : ")
print(df_mean)


