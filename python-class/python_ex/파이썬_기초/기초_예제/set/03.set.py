
# 집합 예제 (두 태수들의 취미 분석)

# 두 태수들의 취미
leetaesoo_hobbies = {"축구", "농구", "게임", "노래", "애니 시청", "얼음 샤워"}
samtaesoo_hobbies = {"축구", "농구", "게임", "노래", "메뚜기의 종류 100가지 외우기"}

common_hobbies = leetaesoo_hobbies & samtaesoo_hobbies
print(f"\n두 태수의 공통 취미 : {common_hobbies}\n")                

only_leetaesoo = leetaesoo_hobbies - samtaesoo_hobbies
print(f"\n이태수만 가진 취미 : {only_leetaesoo}\n")             

only_samtaesoo = samtaesoo_hobbies - leetaesoo_hobbies
print(f"\n삼태수만 가진 취미 : {only_samtaesoo}\n")           

all_hobbies = leetaesoo_hobbies | samtaesoo_hobbies
print(f"\n모든 취미 목록 : {all_hobbies}\n")               

unique_hobbies = leetaesoo_hobbies ^ samtaesoo_hobbies
print(f"\n독특한 취미 : {unique_hobbies}\n")    

print(f"\n전체 취미 종류 수 : {len(all_hobbies)}종류\n")


