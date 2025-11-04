# 데이터 선택(Selecting)과 필터링(Filtering)

import pandas as pd

# 샘플 DataFrame 생성 
df = pd.DataFrame({
    'Name' : ['John', 'Anna', 'Peter', 'Linda', 'Bob'],
    'Age' : [28, 24, 35, 32, 45],
    'City' : ['New York', 'Paris', 'Berlin', 'London', 'Tokyo'],
    'Salary' : [50000, 65000, 75000, 85000, 600000],
    'Department' : ['IT', 'HR', 'IT', 'Finance', 'Maketing']
})

print("단일 열 선택 (Series 반환) : ")
print(df['Name'])

# 여러 열 선택
print("\n여러 열 선택 (DataFrame 반환) : ")
print(df[['Name', 'Salary']])

# 행 선택(위치 기반)
print("\n처음 3행 선택 : ")
print(df.iloc[0:3])

# 행 선택(레이블 기반)
print("\n인덱스 1, 3, 4 행 선택 : ")
print(df.loc[1, 3, 4])

# 특정 행과 열 동시 선택
print("\n첫 2행의 'Name'과 'Age' 열 : ")
print(df.loc[0:1, ['Name', 'Age']])

# 조건부 필터링
print("\n30세 이상인 직원 : ")
print(df[df['Age'] >= 30])

# 다중 조건 필터링
print("\nIT 부서의 30세 이상 직원 : ")
print(df[(df['Age'] >= 30) & (df['Department'] == 'IT')])

# 값 존재 여부 필터링
print("\n도쿄나 런던에 사는 직원 : ")
print(df[(df['City'] >= 30) & (df['Tokyo', 'London'])])