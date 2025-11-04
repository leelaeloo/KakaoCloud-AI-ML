# 데이터 프레임 GroupBy
import pandas as pd

df = pd.DataFrame({
    'Department' : ['IT', 'HR', 'IT', 'Finance', 'HR', 'IT'],
    'Employee' : ['Alice', 'bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'Salary' : [75000, 65000, 85000, 90000, 60000, 78000],
    'Age' : [28, 35, 32, 45, 30, 29],
    'Year' : [2021, 2022, 2021, 2022, 2021, 2022]
})

# 기본 groups 연산
dept_groups = df.groupby('Department')
print("부서별 평균 급여 : ")
print(dept_groups['Salary'].mean())

# 다중 열 기준 그룹화
year_dept_groups = df.groupby(['Year', 'Department'])
print("\n연도별, 부서별 평균 급여 : ")
print(year_dept_groups['Salary'].mean())

# describe()는 각 그룹별로 기본 통계량(개수, 평균, 표준편차, 최소값, 25%, 50%, 75%, 최대값)을 제공함
print("\n부서별 급여 통계 요약 : ")
print(dept_groups['Salary'].describe())

# agg 메소드로 다양한 집계 함수 적용
print("\n여러 집계 함수 적용: ")
print(dept_groups['Salary'].agg(['count', 'mean', 'sum', 'std', 'min', 'max']))
# egg와 describe 차이점
# - egg : 사용자가 원하는 집계 함수들을 직접 선택하여 적용
# - describe : 미리 정의된 통계 요약 정보를 제공 ('count', 'mean', 'sum', 'std', 'min', 'max')

# 열마다 다른 집계 함수 적용
print("\n열별 다른 집계 함수 : ")
print(dept_groups.agg({
    'Salary': ['mean', 'max'],
    'Age': ['mean', 'max', 'max']
}))

# transform 메소드 : 그룹 통계를 원본 데이터 크기로 변환
# transform()은 그룹별 집계 결과를 원본 DataFramer과 같은 크기로 확장하여 반환
df['Dept_Avg_Salary'] = dept_groups['Salary'].transform('mean')
print("\n각 직원의 급여와 부서 평균 급여 : ")
print(df[['Employee', 'Department', 'Salary', 'Dept_Avg_Salary']])

# filter 메소드 : 그룹 조건에 따라 필터링
high_salary_depts = dept_groups.filter(lambda x: x['Salary'].mean() > 70000)
print(high_salary_depts)

# get_group 메소드 : 특정 그룹 선택
print("\nIT 부서 직원 : ")
print(dept_groups.get_group('IT'))