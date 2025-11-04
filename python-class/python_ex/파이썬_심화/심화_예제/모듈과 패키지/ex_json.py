import json

person = {
    'name' : '이태수',
    'age' : 25,
    'skills' : ['Python', 'React'],
    'active' : True
}

json_str = json.dumps(person, ensure_ascii=False, indent=2)
print(f"\nJSON 문자열 : \n{json_str}")

person_dict = json.loads(json_str)
print(f"\n이름 : {person_dict['name']}, 나이 : {person_dict['age']}, 스킬 : {person_dict['skills']}\n")


