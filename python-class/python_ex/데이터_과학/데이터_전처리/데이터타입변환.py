import pandas as pd

df = pd.DataFrame({
    'A' : ['1', '2', '3', '4', '5'],                    # 숫자인데 문자열로 저장됨
    'B' : [1.1, 2.2, 3.3, 4.4, 5.5],                    # 올바른 float 타입
    'C' : ['2020-01-01', '2020-02-01', '2020-03-01',    # 날짜인데 문자열로 저장됨
           '2020-04-01', '2020-05-01'],
    'D' : ['True', 'False','True', 'False','True']      # 불리언인데 문자열로 저장됨
})

print("원본 데이터 타입 : ")
print(df.dtypes)

# 1. 문자열 -> 정수 변환
df['A'] = df['A'].astype(int)
# 수학적 연산이 가능해짐

# 2. 문자열 -> 날짜/시간 변환
df['C'] = pd.to_datetime(df['C'])
# 날짜 연산이 가능해짐

# 3. 문자열 -> 불리언 변환
df['D'] = df['D'].astype(bool)
# 주의 : 문자열 False도 비어있지 않은 문자열 이므로 True로 변환됨

# 올바른 불리언 변환 방법
df_original = pd.DataFrame({
    'D' : ['True', 'False','True', 'False','True']
})

# 불리언 변환 방법 1 : map() 사용
df_original['D_correct1'] = df_original['D'].map({'True': True, 'False' : False})

# 불리언 변환 방법 2 : 조건문 사용
df_original['D_correct2'] = (df_original['D'] == 'True')