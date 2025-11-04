# 집합 연산

# 기본 집합 생성
A = {2, 4, 6, 8, 10}
B = {8, 10, 12, 14, 16}

# 합집합 -> A와 B의 모든 요소
print(A | B)        # {2, 4, 6, 8, 10, 12, 14, 16}
print(A.union(B))   # 위와 동일

# 교집합 -> A와 B 모두에 있는 요소
print(A & B)        # {8, 10}
print(A.intersection(B))  # 위와 동일

# 차집합 -> A에는 있지만 B에는 없는 요소
print(A - B)        # {2, 4, 6}
print(A.difference(B))  # 위와 동일

# 대칭 차집합 -> A 또는 B에 잇찌만 양쪽에 모두 있지는 않은 요소
print(A ^ B)          # {16, 2, 4, 6, 12, 14}
print(A.symmetric_difference(B))

# 부분집합 확인
C = {2, 4}
print(C.issubset(A)) # True (C는 A의 부분 집합)
print(C <= A)        # 위와 동일

# 진부분집합 확인
print(C < A)         # True (C는 A의 진부분집합)

# 상위집합 확인
print(A.issuperset(C))      # True (A는 C의 상위집합)
print(A >= C)               # 위와 동일

# 진상위집합 확인
print(A > C)                # True (A는 C의 진상위집합)

# 서로소 확인
D = {18, 20, 22}            
print(A.isdisjoint(D))      # True (A와 D는 공통 요소가 없음)