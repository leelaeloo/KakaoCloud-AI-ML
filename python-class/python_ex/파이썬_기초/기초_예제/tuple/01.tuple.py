# 튜플 사용 케이스_1

# 다중 반환 값 처리
def get_dimensions():
    width = 1000
    height = 500
    depth = 100
    return width, height, depth


dimensions = get_dimensions()
print(f"튜플 : {dimensions}")                   # 튜플 : (1000, 500, 100)

# 언패킹으로 개별 값 받기
w, h, d = get_dimensions()
print(f"너비 : {w}, 높이 : {h}, 깊이 : {d}")   # 너비 : 1000, 높이 : 500, 깊이 : 100
