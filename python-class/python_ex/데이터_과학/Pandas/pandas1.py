import numpy as np
import pandas as pd
# print(pd.__version__)

# --- Series 생성 및 메소드 --- #

# 기본 Series 생성
s = pd.Series([1, 3, 5, 7, 9])
print(s)

# 인덱스 지정하여 Series 생성
s2 = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print(s2)

# 딕셔너리로 Series 생성
population = {
    'Seoul' : 9776,
    'Busan' : 3429,
    'Incheon' : 2947,
    'Dague' : 2465,
}

pop_series = pd.Series(population)
print(pop_series)

s = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

# 기본 속성
print("값 배열 : ", s.values)
print("인덱스 : ", s.index)

# 기본 통계 메소드
print("평균 : ", s.mean())
print("합계 : ", s.sum())
print("최소값 : ", s.min())
print("최대값 : ", s.max())

# 데이터 접근
print("'c' 인덱스의 값 : ", s['c'])
print("여러 인덱스의 값 : ", s[['a', 'c', 'e']])

# 조건부 필터링
print("30보다 큰 값 : ", s[s > 30])

# 데이터 변환
print("제곱근 : ", s.apply(np.sqrt))
print("2배 값 : ", s * 2)

# 결측치 확인 및 처리
s2 = pd.Series([10, np.nan, 30, np.nan, 50], index=['a', 'b', 'c', 'd', 'e'])
print("결측지 여부 : ", s2.isna())
print("결측지 제외 : ", s2.dropna())
print("결측지 0으로 채우기: ", s2.fillna(0))