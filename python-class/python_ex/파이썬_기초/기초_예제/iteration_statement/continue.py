#continue
# 현재 반복을 중단하고 다음 반복으로 넘어감

# 1. 특정 조건만 처리하기 (짝수만 출력)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for num in numbers:
    if num % 2 != 0: # 홀수이면
        continue # 다음 반복으로 넘어감

    print(f"{num}은(는) 짝수입니다. 제곱: {num**2}")

# 2. 특정 요소 건너뛰기
for i in range(1, 11):
    if i == 7:
        print(f"{i}는 건너뜁니다.")
        continue
    print(f"현재 숫자: {i}")