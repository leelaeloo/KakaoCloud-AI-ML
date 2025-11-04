
import numpy as np
import pandas as pd

# 이상치(Outliers) 탐지 및 제거

# 이상치가 포함된 샘플 데이터 생성
np.random.seed(42)
normal_data = np.random.normal(50, 10, 95)      # 정상 데이터 95개
outliers = [120, 130, -20, -10, 150]            # 이상치 5개
data_with_outliers = np.concatenate([normal_data, outliers])

df = pd.DataFrame({
    'ID' : range(1, 101),
    'Score' : data_with_outliers,
    'Category' : np.random.choice(['A','B', 'C'], 100)
})

print("\n원본 데이터 통계 : ")
print(df['Score'].describe())

# -------------------------- #

# IQR 방법
def detect_outliers_iqr(data):
    Q1 = data.quantile(0.25)        # 1사분위수
    Q3 = data.quantile(0.75)        # 3사분위수
    IQR = Q3 - Q1

    # 이상치 경계값 계산 (일반적으로 1.5 * IQR 사용)
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 - 1.5 * IQR

    # 이상치 식별
    outliers = (data < lower_bound) | (data > upper_bound)
    return outliers, lower_bound, upper_bound

outliers_mask, lower, upper = detect_outliers_iqr(df['Score'])
print(f"\nIQR 방법 = 이상치 경계 : {lower:.2f} ~ {upper:.2f}")
print(f"이상치 개수 : {outliers_mask.sum()}개")
print("이상치 값들 : ")
print(df[outliers_mask]['Score'].values)

# -------------------------- #

# Z-Score 방법
def detect_outliers_zscores(data, threshold=3):
    z_scores = np.abs((data - data.mean()) / data.std())
    outliers = z_scores > threshold
    return outliers, z_scores

outliers_zscore, z_score = detect_outliers_zscores(df['Score'])
print(f"\nZ-Score 방법 - 이상치 개수 : {outliers_zscore.sum()}개")
print("Z-Score가 3 이상인 값들 : ")
print(df[outliers_zscore][['ID', 'Score']].values)

# 이상치 제거
df_no_outliers = df[~outliers_mask].copy()          #  IQR 방법으로 탐지된 이상치 제거
# ~outliers_mask : outliers_maskrk True인 행을 제외
# copy() : 원본 데이터프레임을 복사하여 이상치 제거된 새로운 데이터프레임 생성
print(f"\n이상치 제거 전 데이터 크기 : {len(df)}")
print(f"이상치 제거 후 데이터 크기 : {len(df_no_outliers)}")
print("\n이상치 제거 후 통계 : ")
print(df_no_outliers['Score'].describe())

# 대체값으로 처리
df_replaced = df.copy()
# 이상치를 중앙값으로 대체
median_score = df['Score'].median()
df_replaced.loc[outliers_mask, 'Score'] = median_score
print(f"\n이상치를 중앙값({median_score:.2f})으로 대체 후 통계 : ")
print(df_replaced['Score'].describe())

