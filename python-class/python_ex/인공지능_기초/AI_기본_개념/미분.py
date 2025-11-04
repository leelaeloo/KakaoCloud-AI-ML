import numpy as np
import matplotlib.pyplot as plt

def numerical_derivative(f, x, h=1e-7):
    # 수치적 미분 계산
    # f : 함수
    # x : 미분할 점
    # h : 아주 작은 변화량
    return (f(x + h) - f(x)) / h

def derivative_definition_demo():
    def f(x):
        return x**2
    
    a = 2
    h_values = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001]

    print("미분의 정의 : f'(2) = lim[h+0] [f(2+h) - f(2)] / h")
    print("함수 : f(x) = x2")

    for h in h_values:
        diff_quotient = numerical_derivative(f, a, h)
        print(f"h = {h:8.5f}: [f(2+{h}) - f(2)] / {h} = {diff_quotient:.6f}")

    analytical_derivative = 2 * a
    print(f"\n정확한 미분값 : f'(2) = {analytical_derivative}")
    
    numerical_result = numerical_derivative(f, a)
    print(f"수치적 미분값 : f'(2) = {numerical_result:.6f}")

    return h_values, [f(a + h) for h in h_values]

def plot_derivative_concept():
    # 미분의 기하학적 의미 시작화
    def f(x):
        return x**2
    
    x = np.linspace(0, 4, 100)
    y = f(x)
    
    a = 2
    slope = 2 * a
    
    tangent_x = np.linspace(1, 3, 100)
    tangent_y = f(a) + slope * (tangent_x - a)
    
    plt.rc('font', family='Malgun Gothic')
    plt.figure(figsize=(10, 6))
    
    plt.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')
    
    plt.plot(a, f(a), 'ro', markersize=8, label=f'점 ({a}, {f(a)})')

    plt.plot(tangent_x, tangent_y, 'r--', linewidth=2, 
             label=f'접선 (기울기 = {slope})')
    
    h_values = [1, 0.5, 0.2]
    colors = ['orange', 'green', 'purple']
    
    for i, h in enumerate(h_values):
        x_end = a + h
        y_end = f(x_end)
        
        secant_slope = numerical_derivative(f, a, h)
        
        secant_x = np.array([a, x_end])
        secant_y = np.array([f(a), y_end])
        plt.plot(secant_x, secant_y, '--', color=colors[i],
                 linewidth=1.5, label=f'할선 (h={h}, 기울기={secant_slope:.1f})')
        
        plt.plot(x_end, y_end, 'o', color=colors[i], markersize=6)
        
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('미분의 기하학적 의미 : 할선이 접선으로 수렴')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

plot_derivative_concept()