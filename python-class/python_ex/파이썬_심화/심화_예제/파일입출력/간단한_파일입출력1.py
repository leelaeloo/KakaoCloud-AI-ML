
# 파일에 데이터를 쓰는 부분
print("\n파일에 내용을 저장합니다.\n")

# 'w' 모드로 'test.tx' 파일을 열기
# 파일이 없으면 새로 생성하고, 있으면 기존 내용을 덮어씀
with open("test.txt", "w", encoding='utf-8') as file:
    file.write("오늘은 하루종일 공부를 했다!.\n")
    file.write("내일은 벌써 월요일이다...")

print("파일 저장 완료!")

# 파일에서 데이터를 읽는 부분
print("\n파일에서 내용을 불러옵니다.\n")

# 'r' 모드로 'test.tx' 파일을 열기
# 파일이 없으면 오류가 발생
with open("test.txt", "r", encoding='utf-8') as file:
    # 파일의 모든 내용을 읽어와 'content' 변수에 저장
    content = file.read()
    print("파일 내용:")
    print(content)

print("\n파일 읽기 완료\n")

