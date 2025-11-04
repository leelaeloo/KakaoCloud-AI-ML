# JSON 처리
import requests

# 무료 테스트 API에 GET 요청 보내기
response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

# 응답 상태 확인
if response.status_code == 200:
    data = response.json()

    print(f"게시물 ID : {data['id']}")
    print(f"제목 : {data['title']}")
    print(f"내용 : {data['body']}")
    print(f"작성자 ID : {data['userId']}")

else:
    print(f"오류 발생 : {response.status_code}")
