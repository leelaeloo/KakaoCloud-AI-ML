import csv

# 헤더 (열 이름)
header = ['id', 'name', 'age', 'score']

# 데이터 (행 내용)
data = [
    ['1', '이태수', '25', '85'],
    ['2', '삼태수', '33', '92'],
    ['3', '사태수', '44', '78'],
    ['4', '오태수', '55', '96'],
    ['5', '육태수', '66', '65']
]

# CSV 파일 쓰기
with open('students.csv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)
    
    # 헤더 쓰기
    csv_writer.writerow(header)
    
    # 데이터 쓰기
    csv_writer.writerows(data)

print("students.csv 파일 생성 완료")