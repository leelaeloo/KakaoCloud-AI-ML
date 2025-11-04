# f-string
name = "이태수"
age = 25
message = f"이름 : {name}, 나이 : {age}세"
print(message)

# format
message = "이름 : {}, 나이 : {}세".format(name, age)
print(message)

message = "이름 : {0}, 나이 : {1}세".format(name, age)
print(message)