
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 간단한 집값 예측 머신러닝 모델
def house_price_prediction():
    # 집 크기를 기반으로 집값을 예측하는 머신러닝 모델

    np.random.seed(42)
    # 평균 100평, 표준편차 30, 1000개의 데이터
    house_sizes = np.random.normal(100, 30, 1000)
    print(house_sizes)

    # 실제로는 집값이 크기에만 의존하지 않기 때문에 현재는 노이즈를 추가하는 형태로 데이터 생성
    house_prices = house_sizes * 50 + np.random.normal(0, 500, 1000) + 2000
    print(house_prices)

    #  데이터 전처리
    X = house_sizes.reshape(-1, 1)      # 2D 배열로 변환(행, 열)
    y = house_prices
    
    # 훈련용/테스트용 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 머신러닝 모델 생성 및 훈련
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 예측
    y_pred = model.predict(X_test)

    # 성능 평가
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"평균 제곱 오차 (mse) : {mse:.2f}")
    print(f"결정 계수 (R²) : {r2:.2f}")
    print(f"모델 계수 (기울기) : {model.coef_[0]:.2f}")
    print(f"모델 절편 : {model.intercept_:.2f}")

    # 새로운 집 크기에 대한 예측
    new_house_sizes = [80, 120, 150]
    for size in new_house_sizes:
        predicted_price = model.predict([[size]])[0]
        print(f"{size}평 집의 예상 가격 : {predicted_price:.2f}만원")

    return model, X_test, y_test, y_pred

# 실행
model, X_test, y_test, y_pred = house_price_prediction()

