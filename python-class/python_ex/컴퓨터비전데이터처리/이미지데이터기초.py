import numpy as np
import matplotlib.pyplot as plt

# 3x3 픽셀 이미지
simple_image = np.array([
    [[255, 0, 0], [0, 255, 0], [0, 0, 255]],  # 빨강, 초록, 파랑
    [[255, 255, 0], [255, 0, 255], [0, 255, 255]],  # 노랑, 마젠타, 시안
    [[0, 0, 0], [128, 128, 128], [255, 255, 255]]  # 검정, 회색, 흰색
], dtype=np.uint8)

plt.rc('font', family='Malgun Gothic')
plt.figure(figsize=(8, 4))
plt.imshow(simple_image)
plt.title('3x3 픽셀 이미지')
plt.axis('off')
plt.show()

