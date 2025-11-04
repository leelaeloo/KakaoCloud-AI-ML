
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  

# 데이터셋 불러오기
tips = sns.load_dataset("tips")
iris = sns.load_dataset("iris")

tips = tips.rename(columns={"sex": "gender"})

# 2행 2열 subplot 만들기
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. 산점도 (총 금액 vs 팁, 성별에 따라 색 구분)
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="gender", ax=axes[0, 0])
axes[0, 0].set_title("산점도: 총 금액과 팁의 관계")
axes[0, 0].set_xlabel("총 금액")
axes[0, 0].set_ylabel("팁")

# 2. 박스플롯 (요일별 총 금액 분포, 성별 구분)
sns.boxplot(data=tips, x="day", y="total_bill", hue="gender", ax=axes[0, 1])
axes[0, 1].set_title("박스플롯: 요일별 총 금액 분포")
axes[0, 1].set_xlabel("요일")
axes[0, 1].set_ylabel("총 금액")

# 3. 히트맵 (iris 데이터 상관관계)
corr = iris.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=axes[1, 0])
axes[1, 0].set_title("히트맵: 아이리스 데이터 상관관계")

# 4. KDE(밀도) 그래프 (iris 꽃잎 길이 분포)
sns.kdeplot(data=iris, x="petal_length", hue="species", fill=True, ax=axes[1, 1])
axes[1, 1].set_title("밀도 그래프: 품종별 꽃잎 길이 분포")
axes[1, 1].set_xlabel("꽃잎 길이")
axes[1, 1].set_ylabel("밀도")

plt.tight_layout()
plt.show()

