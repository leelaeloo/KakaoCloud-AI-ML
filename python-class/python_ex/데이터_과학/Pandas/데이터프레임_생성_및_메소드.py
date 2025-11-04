import pandas as pd
# print(pd.__version__)

data = {
    'Name' : ['John', 'Anna', 'Peter', 'Linda', 'Bob'],
    'Age' : [28, 24, 35, 32, 45],
    'City' : ['New York', 'Paris', 'Berlin', 'London', 'Tokyo'],
    'Salary' : [50000, 65000, 75000, 85000, 600000]
}

df = pd.DataFrame(data)
print(df)

# 기본 속성
print("크기(행, 열) : ", df.shape)
print("열 이름 : ", df.columns)
print("행 인덱스 : ", df.index)
print("데이터 타입 : ", df.dtypes)

# 데이터 확인
print("처음 2행\n : ", df.head(2))
print("마지막 2행\n : ", df.tail(2))
print("기본 통계량\n : ", df.describe())

# 데이터 접근
print("'Age' 열 : \n", df['Age'])
print("여러 열 선택 : \n", df[['Name', 'Salary']])
print("첫 3행 : \n", df.iloc[0:3])
print("조건부 선택 : \n", df[df['Age'] > 30])

# 데이터 수정
df['Age'] = df['Age'] + 1
print("모든 나이에 1 추가 : \n", df)
df['Country'] = ['USA', 'France', 'Germany', 'UK', 'Japn']
print("새 열 추가 : \n", df)
df.loc[5] = ['Charlie', 29, 'Sydney', 70000, 'Australia']
print("새 행 추가 : \n", df)
df.drop('Country', axis=1, inplace=True)
df.drop(5, axis=0, inplace=True)
print("열 삭제 : \n", df)
print("행 삭제 : \n", df)