# if 문

total_price = 75000  # 구매 금액
discount_threshold = 50000  # 할인 기준액

# 할인 조건 검사
if total_price > discount_threshold:
    print(f"구매 금액 {total_price}원은 할인 기준액({discount_threshold})원을 초과했습니다.")
    print("10% 할인이 적용됩니다!")
    discount = total_price * 0.10
    final_price = total_price - discount
    print(f"할인금액: {discount:.0f}원")
    print(f"최종 결제금액: {final_price:.0f}원")

print("이용해 주셔서 감사합니다.") # 조건과 무관하게 항상 실행