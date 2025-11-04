
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

import numpy as np
import matplotlib.pyplot as plt

# MNIST 손글씨 숫자를 인식하는 딥러닝 모델
def mnist_deep_learning():
    
    # 1. 데이터 로드 및 전처리
    # MNIST 데이터셋 로드(X는 이미지, Y는 레이블(정답))
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    
    # 첫 번째 이미지 저장
    x_train_one = X_train[0]
    plt.imsave('x_train_one.png', x_train_one, cmap='gray')
    
    print(f"X_train.shape: {X_train.shape}")
    # print(f"X_train[0]: {X_train[0]}")
    # print(f"X_train[0][10]: {X_train[0][10]}")
    # print(f"X_train[0][10][5]: {X_train[0][10][5]}")
    
    # 데이터 정규화 및 형태 변경
    # 모델에 입력하기 위해 이미지 데이터의 형태를 28x28x1로 바꿈
    # -1은 전체 데이터의 개수를 의미하며, 1은 채널(흑백)을 의미
    # astype('float32')는 연산을 위해 데이터 타입을 실수로 변경
    # 255.0으로 나누어 픽셀 값을 0~1 사이로 정규화
    X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
    X_test = X_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0
    
    # 레이블을 원-핫 인코딩
    # 예: 숫자 5는 [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]으로 변환
    y_train = to_categorical(y_train, 10)       # 0 ~ 9까지 총 10개 클래스
    y_test = to_categorical(y_test, 10)
    
    # 2. CNN 모델 구축
    # Sequential()은 층을 순서대로 쌓아 모델을 만듬
    model = Sequential([
        # 첫 번째 합성곱 레이어
        # Conv2D: 이미지의 특징을 추출하는 층
        # 32: 특징 맵(feature map)의 개수
        # (3, 3): 커널(필터)의 크기
        # activation='relu': ReLU 활성화 함수를 사용하여 음수 값을 0으로 만듬
        # input_shape: 입력 데이터의 형태를 지정
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2)),
        
        # 두 번째 합성곱 레이어  
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # 세 번째 합성곱 레이어
        Conv2D(64, (3, 3), activation='relu'),
        
        # 1차원으로 변환
        # Flatten: 2차원 데이터를 1차원 데이터로 변환하여 다음 층으로 전달
        Flatten(),
        
        # 완전 연결 레이어
        # 64: 뉴런의 개수
        Dense(64, activation='relu'),

        # Dropout: 훈련 시 무작위로 일부 뉴런을 비활성화하여 과적합을 방지
        Dropout(0.5),
        
        # 출력 레이어
        # 10: 0~9까지 10개의 숫자를 분류해야 하므로 10개의 뉴런을 가짐
        # activation='softmax': 각 숫자에 대한 확률을 출력합니다. 모든 확률의 합은 1
        Dense(10, activation='softmax')
    ])
    
    # 3. 모델 컴파일
    # optimizer: 모델을 어떻게 최적화할지(학습할지) 결정 'adam'이 가장 널리 사용
    # loss: 모델의 예측이 얼마나 틀렸는지 측정하는 손실 함수
    # metrics: 모델의 성능을 평가할 지표입니다. 여기서는 '정확도'를 사용
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # 4. 모델 훈련
    print("모델 훈련을 시작합니다...")
    print("훈련 과정: CNN이 60,000개 이미지에서 패턴을 학습합니다...")
    
    # model.fit(): 훈련용 데이터로 모델을 학습시킴
    # batch_size: 한 번에 학습할 데이터의 개수
    # epochs: 전체 훈련 데이터를 몇 번 반복해서 학습할지 정함
    # validation_data: 훈련 중 모델의 성능을 검증할 데이터
    history = model.fit(
        X_train, y_train,
        batch_size=128,
        epochs=5,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # 5. 모델 평가
    # model.evaluate(): 테스트용 데이터로 최종 성능을 평가
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"최종 테스트 정확도: {test_accuracy:.4f}")
    print("MNIST 벤치마크: 일반적으로 99% 이상 달성 가능")
    
    # 6. 예측 예시
    # 테스트 데이터에서 무작위로 5개의 이미지를 선택
    sample_idx = np.random.randint(0, len(X_test), 5)
    # 선택된 이미지에 대한 예측을 수행
    predictions = model.predict(X_test[sample_idx])
    
    print("\n예측 예시 테스트:")
    for i, idx in enumerate(sample_idx):
        # 예측된 숫자(가장 높은 확률을 가진 인덱스)를 찾음
        predicted_digit = np.argmax(predictions[i])
        # 실제 숫자(정답)를 찾음
        actual_digit = np.argmax(y_test[idx])
        # 예측의 신뢰도를 백분율로 계산
        confidence = np.max(predictions[i]) * 100
        
        result = "✅" if predicted_digit == actual_digit else "❌"
        print(f"예측 {i+1}: 예측={predicted_digit}, 실제={actual_digit}, 신뢰도={confidence:.1f}%  {result}")
    
    print("CNN 모델 완성! 손글씨 숫자를 높은 정확도로 인식할 수 있습니다.")
    
    return model, history

# 실행
model, history = mnist_deep_learning()