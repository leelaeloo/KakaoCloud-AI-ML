# 집합 과제
# 소셜 네트워크에서 사용자 간의 관계와 추천 시스템을 구현하는 프로그램 작성
# 공통 관심사를 갖는 친구 응답
# 공통 관심사가 없는 친구 응답

taesoo_interests = {

    "이태수": {"운동", "영화", "요리", "애니 시청"},
    "삼태수": {"애니 시청", "스포츠", "여행", "음악", "메뚜기의 종류 100가지 외우기"},
    "사태수": {"프로그래밍", "게임", "영화", "용암 샤워"},
    "오태수": {"요리", "여행", "용암 샤워", "애니 시청", "괴식 먹방"},
    "육태수": {"프로그래밍", "독서", "음악", "물구나무 서서 코딩"},
    "칠태수": {"스포츠", "게임", "음악", "메뚜기의 종류 100가지 외우기","요리", "혼잣말", "애니 시청"}

}

# 분석할 태수 입력
target_taesoo_name = "삼태수"     # 예) target_taesoo_name = "이태수"

# 결과 저장용 리스트와 딕셔너리
common_taesoo = {}
no_common_taesoo = []

# 입력한 태수가 데이터에 있는지 확인
if target_taesoo_name not in taesoo_interests:
    print(f"\n'{target_taesoo_name}'를 찾을 수 없습니다.. \n 정확한 태수 이름을 입력해 주세요! \n" ) 
else:
    target_interests = taesoo_interests[target_taesoo_name]

    # 모든 태수를 한 번만 반복
    for taesoo, interests in taesoo_interests.items():
        if taesoo == target_taesoo_name:
            continue

        # 교집합 연산으로 공통 관심사 찾기
        common = target_interests & interests
        
        # 결과 분류 if/else
        if common:
            common_taesoo[taesoo] = common 
        else:
            no_common_taesoo.append(taesoo) 

    print(f"\n## {target_taesoo_name}와 공통 관심사가 있는 태수 ##\n")
    for taesoo, common in common_taesoo.items():
        print(f"- {taesoo}: {common}\n")

    print(f"\n## {target_taesoo_name}와 공통 관심사가 없는 태수 ##\n")
    for taesoo in no_common_taesoo:
        print(f"- {taesoo}\n")




