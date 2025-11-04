import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# 기본 고객 데이터 생성
n_customers = 1000
customer_data = {
    'customer_id': range(1, n_customers + 1),
    'name': [f'Customer_{i}' for i in range(1, n_customers + 1)],
    'age': np.random.normal(35, 12, n_customers).astype(int),
    'gender': np.random.choice(['M', 'F', 'Male', 'Female', 'm', 'f', ''], n_customers),
    'city': np.random.choice(['Seoul', 'Busan', 'Daegu', 'Incheon', 'Gwangju', ''], n_customers),
    'total_purchase': np.random.exponential(50000, n_customers),
    'purchase_count': np.random.poisson(5, n_customers),
    'last_purchase_days': np.random.randint(1, 365, n_customers),
    'membership_level': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum', ''], n_customers)
}

df = pd.DataFrame(customer_data)

print("\n --- 1단계 : 원본 데이터 탐색 ---")
print(f"데이터 크기 : {df.shape}")
print(f"\n 데이터 타입 : ")
print(df.dtypes)
print(f"\n처음 5행 : ")
print(df.head())

print("1. 결측치 현황 : ")
missing_data = df.isnull().sum()
missing_percentage = (missing_data / len(df)) * 100
missing_summary = pd.DataFrame({
    '결측치_개수' : missing_data,
    '결측치_비율(%)' : missing_percentage
})

print(missing_summary[missing_summary['결측치_개수'] > 0])

# 2. 데이터 타입 문제 확인  
print(f"\n2. 데이터 타입 문제:")
print(f"나이 데이터 타입: {df['age'].dtype}")
print(f"나이 범위: {df['age'].min()} ~ {df['age'].max()}")
print(f"비정상적인 나이 값: {df[(df['age'] < 0) | (df['age'] > 100)]['age'].tolist()}")

# 3. 범주형 데이터 일관성 문제
print(f"\n3. 성별 데이터 일관성 문제:")
print(f"성별 고유값: {df['gender'].unique()}")
print(f"성별 값 개수: {df['gender'].value_counts()}")

# 4. 이상치 확인 (구매 금액)
print(f"\n4. 구매 금액 이상치 확인:")
Q1 = df['total_purchase'].quantile(0.25)
Q3 = df['total_purchase'].quantile(0.75)
IQR = Q3 - Q1
outlier_threshold_low = Q1 - 1.5 * IQR
outlier_threshold_high = Q3 + 1.5 * IQR
outliers = df[(df['total_purchase'] < outlier_threshold_low) | 
              (df['total_purchase'] > outlier_threshold_high)]
print(f"이상치 개수: {len(outliers)}개 ({len(outliers)/len(df)*100:.1f}%)")
print(f"이상치 범위: {outlier_threshold_low:.0f} 미만 또는 {outlier_threshold_high:.0f} 초과")

# 5. 중복 데이터 확인
print(f"\n5. 중복 데이터 확인:")
duplicates = df.duplicated()
print(f"완전 중복 행: {duplicates.sum()}개")
name_duplicates = df.duplicated(subset=['name'])
print(f"이름 중복: {name_duplicates.sum()}개")

print("--- 2단계 : 데이터 정체 시작 ---")

# 원본 데이터 백업
df_original = df.copy()
print(f"원본 데이터 백업 완료 : {len(df_original)}행")

# 2-1. 나이 데이터 정체
print("\n2-1. 나이 데이터 정체")
print(f"정체 전 나이 범위 : {df['age'].min()} ~ {df['age'].max()}")

# median
# 비정상적인 나이 값을 중앙값으로 대체
median_age = df[(df['age'] >= 0) & (df['age'] <= 100)]['age'].median()
df.loc[(df['age'] < 0) | (df['age'] > 100), 'age'] = median_age

print(f"정제 후 나이 범위: {df['age'].min()} ~ {df['age'].max()}")
print(f"나이 중앙값으로 대체: {median_age}세")

# 온라인 쇼핑몰의 고객 데이터를 분석하기 위해 데이터 전처리를 수행
print(f"\n2-2. 성별 데이터 표준화")
print(f"표준화 전 성별 값: {df['gender'].unique()}")

# 성별 데이터 표준화 매핑
gender_mapping = {
    'M': 'Male', 'm': 'Male', 'Male': 'Male',
    'F': 'Female', 'f': 'Female', 'Female': 'Female',
    '': 'Unknown'
}

df['gender'] = df['gender'].map(gender_mapping).fillna('Unknown')
# map(gender_mapping) : gender_mapping 딕셔너리에 따라 값 매핑
# fillna('Unknown') : 매핑된 값이 None인 경우 'Unknown'으로 대체
print(f"표준화 후 성별 값: {df['gender'].unique()}")
print(f"성별 분포:\n{df['gender'].value_counts()}")

# 도시 데이터 결측치 처리
print(f"\n2-3. 도시 데이터 결측치 처리")
print(f"결측치 처리 전 도시 분포 :\n {df['city'].value_counts()}")

# 빈 문자열을 NaN으로 변환 후 최빈값으로 대체
df['city'] = df['city'].replace('', np.nan)
most_common_city = df['city'].mode()[0]
# fillna(most_common_city) : NaN 값을 최빈값으로 대체

print(f"결측치 처리 후 도시 분포 :\n {df['city'].value_counts()}")
print({f"최빈값 ' {most_common_city}'로 결측치 대체"})

# 멤버십 레벨 결측치 처리
print("\n2-4. 멤버십 레벨 결측치 처리")
df['membership_level'] = df['membership_level'].replace('', 'Bronze')
print(f"멤버심 레벨 분포 : \n{df['membership_level'].value_counts()}")

# 구매 금액 이상치 처리
print("\n3-1. 구매 금액 이상치 처리")
print(f"이상치 처리 전 구매 금액 통계 : ")
print(df['total_purchase'].describe())

# IQR 방법으로 이상치 탐지 및 처리
Q1 = df['total_purchase'].quantile(0.25)
Q3 = df['total_purchase'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 이상치를 경계값으로 대체 (Winsorization)
df.loc[df['total_purchase'] < lower_bound, 'total_purchase'] = lower_bound
df.loc[df['total_purchase'] > upper_bound, 'total_purchase'] = upper_bound

print(f"이상치 처리 후 구매 금액 통계:")
print(df['total_purchase'].describe())

# 파생 변수 생성
print(f"\n3-2. 파생 변수 생성")

# 평균 구매 금액 계산
df['avg_purchase_amount'] = df['total_purchase'] / df['purchase_count']
df['avg_purchase_amount'] = df['avg_purchase_amount'].fillna(0) # 구매 횟수가 0인 경우

# 고객 세그먼트 생성
df['customer_segment'] = 'Regular'
df.loc[(df['total_purchase'] > df['total_purchase'].quantile(0.8)) & 
       (df['last_purchase_days'] < 30), 'customer_segment'] = 'VIP'
df.loc[(df['total_purchase'] < df['total_purchase'].quantile(0.2)) | 
       (df['last_purchase_days'] > 180), 'customer_segment'] = 'At_Risk'

print(f"고객 세그먼트 분포:\n{df['customer_segment'].value_counts()}")

# 온라인 쇼핑몰의 고객 데이터를 분석하기 위해 데이터 전처리를 수행
# 순서가 있는 범주형 데이터
membership_order = {'Bronze': 1, 'Silver': 2, 'Gold': 3, 'Platinum': 4}
df['membership_level_encoded'] = df['membership_level'].map(membership_order)
# map(membership_order): membership_order 딕셔너리에 따라 값 매핑
print(df[['membership_level', 'membership_level_encoded']].head())

# 순서가 없는 범주형 데이터
df_encoded = pd.get_dummies(df, columns=['gender', 'city'], prefix=['gender', 'city'])
print(f"인코딩 후 열 개수: {len(df_encoded.columns)}개")
print(f"새로 생성된 열: {[col for col in df_encoded.columns if col not in df.columns]}")
print(df_encoded.head())

# 수치형 데이터 정규형
print("\n4-1 수치형 데이터 정규화")

numeric_columns = ['age', 'total_purchase', 'purchase_count',
                    'last_purchase_days', 'avg_purchase_amount']

# 정규화 전 데이터 검증 및 정제 p169
print("정규화 전 데이터 검증:")

for col in numeric_columns:
    # 무한대 값 확인
    inf_count = np.isinf(df[col]).sum()
    # NaN 값 확인
    nan_count = df[col].isnull().sum()
    # 극값 확인
    extreme_values = df[col][(df[col] > 1e10) | (df[col] < -1e10)]
    print(f"{col}: 무한대 값 {inf_count}개, NaN 값 {nan_count}개, 극값 {len(extreme_values)}개")
    
    # 무한대 값을 NaN으로 변환
    df[col] = df[col].replace([np.inf, -np.inf], np.nan)

    # NaN 값을 중앙값으로 대체
    if df[col].isnull().sum() > 0:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f" -> {col}의 결측치를 중앙앖 {median_val:.2f}로 대체")

        # 극값 처리 (
        upper_limit = df[col].quantile(0.999)
        lower_limit = df[col].quantile(0.001)

        extreme_mask = (df[col] > upper_limit) | (df[col] < lower_limit)
        if extreme_mask.sum() > 0:
            df.loc[df[col] > upper_limit, col] = upper_limit
            df.loc[df[col] < lower_limit, col] = lower_limit
            print(f" -> {col}의 극값 {extreme_mask.sum()}개를 {lower_limit:.2f}~{upper_limit:.2f} 범위로 제한")

# 정규화 전 통계
print("\n정규화 전 통계 : ")
print(df[numeric_columns].describe())

# 데이터 유효성 최종 확인
print("\n데이터 유효성 최종 확인 : ")
for col in numeric_columns:
    has_inf = np.isinf(df[col]).any()
    has_nan = df[col].isnull().any()
    print(f"{col} :  무한대값 {has_inf}, NaN값 {has_nan}")

# StandardScaler를 사용한 표준화
scaler = StandardScaler()
df_scaled = df_encoded.copy()

try:
    df_scaled[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    print("\n정규화 성공!")
except Exception as e:
    print(f"\n정규화 실패 : {e}")

    for col in numeric_columns:
        print(f"{col} 범위 : {df[col].min():.2f} ~ {df[col].max():.2f}")
        print(f"{col} 평균 : {df[col].mean():.2f}, 표준편차 : {df[col].std():.2f}")

print("\n정규화 후 통계 : ")
print(df_scaled[numeric_columns].describe())

print("\n4-2. 최종 데이터 품질 검증")

print(f"최종 데이터 크기 : {df_scaled.shape}")
print(f"결측치 확인 : {df_scaled.isnull().sum().sum()}개")
print(f"중복 행 확인 : {df_scaled.duplicated().sum()}개")

print("\n --- 데이터 전처리 완료 리포트 ---")
print(f"원본 데이터 : {df_original.shape[0]}행 {df_original.shape[1]}열")
print(f"최종 데이터 : {df_scaled.shape[0]}행 {df_scaled.shape[1]}열")
print(f"처리된 문제들 : ")
print(f"    - 나이 이상치 {len(df_original[(df_original['age'] < 0) | (df_original['age'] > 100)])}개 수정")
print(f"    - 성별 데이터 표준화 완료")
print(f"    - 도시 결측치 {df_original['city'].isnull().sum()}개 처리")
print(f"    - 구매 금액 이상치 처리 완료")
print(f"    - 파생 변수 2개 생성 (평균 구매 금액, 고객 세그먼트)")
print(f"    - 범주형 데이터 인코딩 완료")
print(f"    - 수치형 데이터 표준화 완료")

print(f"\n데이터 전처리가 성공적으로 완료되었습니다!")
print(f"이제 머신러닝 모델 학습이나 데이터 분석에 사용할 수 있습니다.")
