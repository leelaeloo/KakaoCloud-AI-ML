# 중첩 조건문

def analyze_grade(score):
    # 점수가 유효한 범위(0~100) 안에 있는지 확인
    if 0 <= score <= 100:
        if score >= 60:
            return f"점수 {score}: 합격입니다."
        else:
            return f"점수 {score}: 불합격입니다."
    else:
        return f"점수 {score}: 유효하지 않은 점수입니다."

test_scores = [95, 85, 75, 55, 45, 105, -5]

for score in test_scores:
    result = analyze_grade(score)
    print(result)
    print("-" * 25)