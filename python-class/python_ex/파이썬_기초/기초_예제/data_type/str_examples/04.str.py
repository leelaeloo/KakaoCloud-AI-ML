# 문자열 변환 메서드
text = "Lee Tae Soo"
print(text.upper())     # LEE TAE SOO
print(text.lower())     # lee tae soo
print(text.title())     # Lee Tae Soo
print(text.swapcase())  # lEE tAE sOO

# 검색 메서드
print(text.find("Tae"))     # 4
print(text.find("o"))       # 9
print("Soo" in text)        # True

# 변형 메서드
print(" Python ".strip())       # 양쪽 공백 제거 -> "Python"
print(text.split(" "))          # ['Lee', 'Tae', 'Soo']
print("-".join(["L", "E", "E"]))    # L-E-E

# 검증 메서드
print("12345".isdigit())        # 모두 숫자면 True
print("abcde".isalpha())        # 모두 알파벳이면 True
print("LeeTaesoo5".isalnum())   # 숫자 또는 알파벳이면 True