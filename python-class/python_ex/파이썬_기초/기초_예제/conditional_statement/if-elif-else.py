# if-elif-else 문

order_amount = 45000  # 주문금액

if order_amount >= 60000:
    shipping_fee = 0
    message = "무료 배송입니다."
elif order_amount >= 40000:
    shipping_fee = 2000
    message = "일반 배송비가 적용됩니다."
else:
    shipping_fee = 4000
    message = "소액 주문 배송비가 적용됩니다."

total = order_amount + shipping_fee

print(f"주문금액: {order_amount}원")
print(f"배송비: {shipping_fee}원 ({message})")
print(f"최종 결제금액: {total}원")