
# 데이터 프레임 GroupBy 고급
import pandas as pd

df = pd.DataFrame({
    'Department' : ['IT', 'HR', 'IT', 'Finance', 'HR', 'IT'],
    'Employee' : ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'Salary' : [75000, 65000, 85000, 90000, 60000, 78000],
    'Age' : [28, 35, 32, 45, 30, 29],
    'Year' : [2021, 2022, 2021, 2022, 2021, 2022]
})

# 1. 시간 기반 그룹화(월별, 분기별, 연도별)
df['Date'] = pd.date_range(start='2022-01-01', periods=len(df), freq='ME')
print("\n월별 평균 급여:")
print(df.groupby(df['Date'].dt.month)['Salary'].mean())

print("\n분기별 평균 급여:")
print(df.groupby(df['Date'].dt.quarter)['Salary'].mean())

# 2. 연속 변수의 범주화 후 그룹화(구간별 그룹)
df['Age_Group'] = pd.cut(df['Age'], bins=[20, 30, 40, 50], labels=['20대', '30대', '40대'])
print("\n연령대별 평균 급여:")
print(df.groupby('Age_Group', observed=True)['Salary'].mean())

# 3. 크기 기반 분위수로 그룹화
df['Salary_Quantile'] = pd.qcut(df['Salary'], q=3, labels=['Low', 'Medium', 'High'])
print("\n급여 분위수별 평균 나이:")
print(df.groupby('Salary_Quantile', observed=True)['Age'].mean())

# 4. 사용자 정의 함수로 그룹화
# apply() 메소드와 사용자 정의 함수를 결합하여 복잡한 그룹 기준을 만들 수 있음
def experience_level(age):  
    # 나이를 기준으로 경력 수준을 분류하는 함수
    if age < 30:
        return 'Junior'
    elif age < 40:
        return 'Mid-level'
    else:
        return 'Senior'
    
df['Experience'] = df['Age'].apply(experience_level)
print("\n경력 수준별 평균 급여:")
print(df.groupby('Experience')['Salary'].mean())

