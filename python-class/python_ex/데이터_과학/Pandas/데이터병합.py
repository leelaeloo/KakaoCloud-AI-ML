# 데이터 병합
import pandas as pd

# 샘플 데이터 : 고객 정보
customers = pd.DataFrame({
    'customer_id' : [1, 2, 3, 4, 5],
    'name' : ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'email' : ['alice@example.com', 'bob@example.com', 'charlie@example.com',
               'david@example.com', 'eve@example.com']
})

# 샘플 데이터 : 주문 정보
orders = pd.DataFrame({
    'orders_id' : [101, 102, 103, 104, 105],
    'customer_id' : [1, 2, 3, 6, 7],
    'product' : ['Laptop', 'Phone', 'Tablet', 'Monitoer', 'Keyboard'],
    'amount' : [1200, 800, 450, 300, 80]
})

print("고객 정보 : ")
print(customers)
print("\n주문 정보 : ")
print(orders)

# 내부 조인(Inner Join) : 양쪽 모두에 있는 데이터만
inner_join = pd.merge(customers, orders, on='customer_id')
print("\n내부 조인(고객 + 주문) : ")
print(inner_join)

# 왼쪽 조인(Left Join) : 왼쪽 데이터 프레임의 모든 행 포함
left_join = pd.merge(customers, orders, on='customer_id', how='left')
print("\n왼쪽 조인(모든 고객, 주문 없으면 NaN) : ")
print(left_join)

# 오른쪽 조인(Right Join) : 오른쪽 데이터 프레임의 모든 행 포함
right_join = pd.merge(customers, orders, on='customer_id', how='right')
print("\n오른쪽 조인(모든 고객, 주문 없으면 NaN) : ")
print(right_join)

# 외부 조인(Outer Join) : 양쪽 데이터 프레임의 모든 행 포함
outer_join = pd.merge(customers, orders, on='customer_id', how='outer')
print("\n외부 조인(모든 고객 및 주문) : ")
print(outer_join)