# if-else 문

exam_score = 85 # 시험 점수
pass_threshold = 70 # 합격 기준

if exam_score >= pass_threshold:
    print(f"축하합니다! {exam_score}점으로 합격입니다.")
else:
    points_needed = pass_threshold - exam_score
    print(f"아쉽게도 {exam_score}점으로 불합격입니다.")
    print(f"합격까지 {points_needed}점이 부족합니다.")