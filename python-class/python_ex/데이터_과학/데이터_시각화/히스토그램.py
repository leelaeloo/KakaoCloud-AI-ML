
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 샘플 데이터 생성
np.random.seed(42)

# 1. 기본 히스토그램 - 학생 성적 데이터
scores = np.random.normal(75, 15, 1000)  # 평균 75점, 표준편차 15점

plt.figure(figsize=(15, 10))

# 1-1. 기본 히스토그램
plt.subplot(2, 3, 1)
plt.hist(scores, bins=20, color='skyblue', alpha=0.7, edgecolor='black')
plt.title('기본 히스토그램 - 학생 성적')
plt.xlabel('점수')
plt.ylabel('빈도')

# 1-2. 구간(bins) 개수 조정
plt.subplot(2, 3, 2)
plt.hist(scores, bins=10, color='lightgreen', alpha=0.7, edgecolor='black')
plt.title('구간 수 조정 (bins=10)')
plt.xlabel('점수')
plt.ylabel('빈도')

# 1-3. 정규화된 히스토그램 (확률밀도)
plt.subplot(2, 3, 3)
plt.hist(scores, bins=25, density=True, color='orange', alpha=0.7, edgecolor='black')
plt.title('정규화된 히스토그램 (확률밀도)')
plt.xlabel('점수')
plt.ylabel('확률밀도')

# 2. 여러 데이터 비교
class_a = np.random.normal(70, 12, 500)  # A반 성적
class_b = np.random.normal(78, 10, 500)  # B반 성적

plt.subplot(2, 3, 4)
plt.hist(class_a, bins=20, alpha=0.6, label='A반', color='red')
plt.hist(class_b, bins=20, alpha=0.6, label='B반', color='blue')
plt.title('두 반 성적 비교')
plt.xlabel('점수')
plt.ylabel('빈도')
plt.legend()

# 3. 나이대별 분포
ages = np.concatenate([
    np.random.normal(25, 3, 300),   # 20대
    np.random.normal(35, 4, 400),   # 30대  
    np.random.normal(45, 5, 300)    # 40대
])

plt.subplot(2, 3, 5)
plt.hist(ages, bins=30, color='purple', alpha=0.7, edgecolor='black')
plt.title('연령 분포')
plt.xlabel('나이')
plt.ylabel('빈도')

# 4. 수직선과 통계 정보 추가
plt.subplot(2, 3, 6)
plt.hist(scores, bins=25, color='gold', alpha=0.7, edgecolor='black')
plt.axvline(np.mean(scores), color='red', linestyle='--', linewidth=2, label=f'평균: {np.mean(scores):.1f}')
plt.axvline(np.median(scores), color='green', linestyle='--', linewidth=2, label=f'중앙값: {np.median(scores):.1f}')
plt.title('통계 정보가 포함된 히스토그램')
plt.xlabel('점수')
plt.ylabel('빈도')
plt.legend()

plt.tight_layout()
plt.show()

# 5. Pandas를 이용한 고급 히스토그램
print("\n=== Pandas 히스토그램 예제 ===")

# 데이터프레임 생성
df = pd.DataFrame({
    '수학': np.random.normal(80, 15, 200),
    '영어': np.random.normal(75, 12, 200),
    '과학': np.random.normal(78, 18, 200)
})

# 여러 컬럼 한번에 히스토그램
plt.figure(figsize=(12, 4))
df.hist(bins=15, alpha=0.7, figsize=(12, 4))
plt.suptitle('과목별 성적 분포')
plt.show()

# 6. 히스토그램 통계 정보 출력
print("\n=== 히스토그램 분석 결과 ===")
print(f"학생 성적 통계:")
print(f"  평균: {np.mean(scores):.2f}점")
print(f"  중앙값: {np.median(scores):.2f}점")
print(f"  표준편차: {np.std(scores):.2f}점")
print(f"  최솟값: {np.min(scores):.2f}점")
print(f"  최댓값: {np.max(scores):.2f}점")


# 구간별 빈도 계산
counts, bins = np.histogram(scores, bins=10)
print(f"\n구간별 빈도:")
for i in range(len(counts)):
    print(f"  {bins[i]:.1f}~{bins[i+1]:.1f}점: {counts[i]}명")

    