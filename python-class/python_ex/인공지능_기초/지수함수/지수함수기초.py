import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def visualize_exponential_functions():
    # 지수함수의 기본 형태를 시각화
    x = np.linspace(-3, 3, 1000)

    y1 = 2**x
    y2 = 3**x
    y3 = np.exp(x)

    y4 = (0.5)**x
    y5 = (0.3)**x

    plt.figure(figsize=(12, 8))

    plt.plot(x, y1, 'r-', linewidth=2, label='2^x')
    plt.plot(x, y2, 'g-', linewidth=2, label='3^x')
    plt.plot(x, y3, 'b-', linewidth=2, label='e^x')

    plt.plot(x, y4, 'r--', linewidth=2, label='(1/2)^x')
    plt.plot(x, y5, 'g--', linewidth=2, label='(1/3)^x')

    plt.plot(0, 1, 'ko', markersize=8, label='Common Point (0, 1)')

    plt.axhline(y=0, color='k', linestyle=':', alpha=0.7)
    plt.axvline(x=0, color='k', linestyle=':', alpha=0.3)

    plt.xlim(-3, 3)
    plt.ylim(0, 8)

    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    
    plt.title('Exponential Functions Comparison\n'
          'Solid lines: a>1 (increasing)\n' \
          'Dashed lines: 0<a<1 (decreasing)', fontsize=14)
    
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    visualize_exponential_functions()
