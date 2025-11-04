import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# 다양한 스케일의 데이터가 포하된 샘플 데이터 생성
np.random.seed(42)
data = {
    'Age' : np.random.randint(20, 70, 100),
    'Salary' : np.random.normal(50000, 15000, 100),
    'Experience' : np.random.exponential(5, 100),
    'Score' : np.random.uniform(0, 100, 100)
}

df = pd.DataFrame(data)
df['Salary'] = df["Salary"].clip(lower=20000)
df['Experience'] = df["Experience"].clip(upper=20)

print("원본 데이터 통계 : ")
print(df.describe())

# 평균 0 , 표준편차 1로 변환
scaler_standard = StandardScaler()
df_standardized = pd.DataFrame(
    scaler_standard.fit_transform(df),
    columns=df.columns
)

print("표준화 후 통계 : ")
print(df_standardized.describe())

# 0-1 범위로 벼환
scaler_minmax = MinMaxScaler()
df_normalized = pd.DataFrame(
    scaler_minmax.fit_transform(df),
    columns=df.columns
)

print("정규화 후 통계 : ")
print(df_normalized.describe())

# 중앙값괴 IQR 사용
# 로버스트 스케일링은 이상치에 덜 민감함
scaler_robust = RobustScaler()
df_robust = pd.DataFrame(
    scaler_robust.fit_transform(df),
    columns=df.columns
)

print("로버스트 스케일링 후 통계 : ")
print(df_robust.describe())