def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count+=1

counter = count_up_to(5)
print(f"제너레이터 출력 : {next(counter)}")
print(f"제너레이터 출력 : {next(counter)}")
print(f"제너레이터 출력 : {next(counter)}")

for num in count_up_to(3):
    print(f"for 루프 출력 : {num}")