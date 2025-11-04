import csv

def read_csv_to_dict_list(filepath):
    students = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['id'] = int(row['id'])
                row['age'] = int(row['age'])
                row['score'] = int(row['score'])
                students.append(row)
    except FileNotFoundError:
        print(f"오류: 파일 '{filepath}'를 찾을 수 없습니다.")
        return None
    return students

def filter_by_score(students_list, min_score=80):
    filtered_students = []
    for student in students_list:
        if student['score'] >= min_score:
            filtered_students.append(student)
    return filtered_students

def calculate_average_age(students_list):
    if not students_list:
        return 0
    
    total_age = 0
    for student in students_list:
        total_age += student['age']
    
    average_age = total_age / len(students_list)
    return average_age

file_path = "students.csv"

students_data = read_csv_to_dict_list(file_path)

if students_data:
    print("--- 모든 학생 데이터 ---")
    for student in students_data:
        print(student)

    high_score_students = filter_by_score(students_data, 80)
    print("\n--- 성적 80점 이상인 학생 ---")
    for student in high_score_students:
        print(student)

    avg_age = calculate_average_age(high_score_students)
    print(f"\n필터링된 학생들의 평균 나이: {avg_age:.2f}세")