# 반올림 사용
result = round(0.3 + 0.4, 1)        # 0.7

# decimal 모듈 사용(정확한 10진수 연산)
from decimal import Decimal
a = Decimal('0.3')
b = Decimal('0.4')
print(a + b)        # 0.7

# math 모듈의 isclose 함수 사용
import math
print(math.isclose(0.3 + 0.4, 0.7))     # True