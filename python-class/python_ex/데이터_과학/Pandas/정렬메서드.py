 # 데이터 프레임 정렬 메서드
import pandas as pd

df = pd.DataFrame({
    'Name' : ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'Score' : [85, 92, 96, 88, 73],
    'Attendance' : [95, 80, 90, 75, 85, 92]
})

# 점수 기준 상위 3명
print("점수 기준 상위 3명 : ")
print(df.nlargest(3, 'Score'))

# 출석률 기준 하위 2명
print("\n출석률 기준 하위 2명 : ")
print(df.nsmallest(2, 'Attendance'))

# 여러 열 기준 정렬(다중 기준)
print("\n점수와 출석률 모두 높은 상위 3명 : ")
print(df.nlargest(3, ['Score', 'Attendance']))

# sort_values 메소드
print("\n점수 기준 내림차순 정렬 : ")
print(df.sort_values('Score', ascending=False))

print("\n여러 열 기준 정렬 (점수, 내림차순, 출석률 오름차순) : ")
print(df.sort_values(['Score', 'Attendance'], ascending=[False, True]))

# 상관관계 및 공분산
print("\n점수와 출석률의 상관관계 : ")
print(df[df['Score', 'Attendance']].corr)
print("\n점수와 출석률의 공분산 : ")
print(df[df['Score', 'Attendance']].cov)
