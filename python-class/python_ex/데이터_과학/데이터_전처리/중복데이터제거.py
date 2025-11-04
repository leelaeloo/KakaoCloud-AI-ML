import pandas as pd
import numpy as np

# 중복 데이터가 포함된 샘플 데이터
data = {
    'Name' : ['Alcie', 'Bob', 'Charlie', 'Alice', 'David', 'Bod', 'Eve', 'Charlie'],
    'Age' : [25, 30, 35, 25, 40, 30, 28, 35],
    'City' : ['Seoul', 'Busan', 'Seoul', 'Seoul', 'Daegu', 'Busan', 'Seoul','Seoul'],
    'Salary' : [50000, 60000, 70000, 50000, 80000, 65000, 55000, 70000]
}

df = pd.DataFrame(data)
print("원본 데이터")
print(df)
print(f"\n원본 데이터 크기 : {len(df)}행")

# 완전 중복 행 확인
print("\n --- 완전 중복 행 탐지 ---")
duplication_rows = df.duplicated()          # 모든 열이 동일한 행 탐지
print("중복 행 여부 : ")
print(duplication_rows)
print(f"완전 중복 행 개수 : {duplication_rows.sum()}개")

# 특정 열 기분 중복 확인
print("\n --- 특정 열 기준 중복 탐지 ---")
name_duplication = df.duplicated(subset=['Name'])
print("이름 기준 중복 행 : ")
print(df[name_duplication])

name_age_duplicated = df.duplicated(subset=['Name', 'Age'])         # 이름 + 나이 기준 중복
print("\n이름 + 나이 기준 중복 행 : ")
print(df[name_age_duplicated])

# 완전 중복 행 제거
df_no_duplicates = df.drop_duplicates()
print(f"완전 중복 제거 후 : {len(df_no_duplicates)}행")
print(df_no_duplicates)

# 특정 열 기준 중복 제거
df_unique_names = df.drop_duplicates(subset=['Name'])
print(f"\n이름 기준 중복 제거 후 : {len(df_unique_names)}행")
print(df_unique_names)

# 조건부 중복 제거
print("\n --- 조건부 중복 제거(최고 급여 유지) ---")
df_max_salary = df.loc[df.groupby('Name')['Salary'].idxmax()]
print("각 이름별 최고 급여 데이터만 유지 : ")
print(df_max_salary.sort_values('Name'))

# 중복 데이터 통계 요약
print("\n --- 중복 데이터 요약 통계 ---")
total_rows = len(df)
unique_row = len(df.drop_duplicates())
duplicates_count = total_rows - unique_row
duplicate_percentage = (duplicates_count / total_rows) * 100