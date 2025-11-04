

from urllib import request, parse


url = "https://httpbin.org/get"
with request.urlopen(url) as response:
    data = response.read().decode('utf-8')
    print(f"\n응답 데이터 : {data[:100]} ...\n")

params = {'q' : '파이썬 프로그래밍', 'lang' : 'ko'}
query_stirng = parse.urlencode(params)
print(f"\n인코딩된 쿼리 문자열 : {query_stirng}\n")

search_url = f"https://example.com/search?{query_stirng}"
print(f"\n검색 URL : {search_url}\n")

