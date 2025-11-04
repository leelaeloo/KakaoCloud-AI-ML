# 문자열 불변성
text = "Python"
# text = [0] = "X"    # 오류 발생하므로 주석처리

text = "Python"
new_text = text.replace("P", "X")   # "Python"은 그대로 "Xython"이라는 새로운 문자열 생성
print(new_text)

text += " Funny"    # "Python Funny"라는 새로운 문자열 생성 text가 이를 참고
print(text)