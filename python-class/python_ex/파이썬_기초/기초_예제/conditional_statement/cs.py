# 조건문

is_hungry = True # 배가 고프다
is_restaurant_open = True # 식당이 문을 열었다

# 의사결정 과정
if is_hungry:
    print("배가 고프니 밥을 먹으러 갑니다.")
    if is_restaurant_open:
        print("식당으로 가서 맛있는 것을 먹습니다.")
    else:
        print("집에서 요리를 해 먹습니다.")
else:
    print("배가 부릅니다. 밥을 먹지 않습니다.")