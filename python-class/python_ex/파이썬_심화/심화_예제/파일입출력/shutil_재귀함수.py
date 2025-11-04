
import os 
import shutil 


# 예제 폴더 구조를 생성
print(">>> 예제 폴더 구조 생성 중...")
try:
    # os.makedirs()를 사용하여 'source' 폴더와 그 하위 폴더인 'test_folder1'을 한 번에 생성
    # exist_ok=True 옵션은 폴더가 이미 존재하더라도 오류를 발생시키지 않도록 함
    os.makedirs('source/test_folder1', exist_ok=True)
    
    # 'with open(...)' 구문을 사용하여 'source' 폴더 안에 'test1.txt' 파일을 생성하고 내용을 씀
    # 'w' 모드는 쓰기 모드로, 파일이 없으면 새로 만들고 있으면 덮어쑴
    with open('source/test1.txt', 'w') as f:
        f.write('This file is shutil test file1.')
    
    # 'source/test_folder1' 폴더 안에 'test2.txt' 파일을 생성하고 내용을 씀
    with open('source/test_folder1/test2.txt', 'w') as f:
        f.write('This file is shutil test file2.')
        
    print("폴더 구조 생성 완료.\n")
except OSError as e:
    # 폴더 생성 시 권한 문제 등 오류가 발생하면 메시지를 출력하고 프로그램을 종료
    print(f"오류: 폴더 생성에 실패했습니다. {e}")
    exit()

# 재귀 함수를 사용해 폴더 내용 삭제
print("\n>>> 재귀 함수를 사용해 폴더 내용 삭제하기")

def delete_contents_recursively(path):
    # 재귀 함수: 주어진 경로의 모든 파일과 폴더를 삭제
    
    # 재귀 호출의 '종료 조건': 경로가 존재하지 않으면 함수를 종료
    if not os.path.exists(path):
        return

    # 현재 경로의 모든 파일과 폴더를 순회
    for item in os.listdir(path):
        item_path = os.path.join(path, item) # 올바른 경로를 결합
        
        # 항목이 폴더인지 확인
        if os.path.isdir(item_path):
            # 폴더인 경우, 함수 자기 자신을 다시 호출(재귀 호출)
            delete_contents_recursively(item_path)
            
            # 하위 폴더의 내용이 모두 삭제되면, 빈 폴더를 제거
            os.rmdir(item_path)
            print(f"폴더 삭제: {item_path}")
        else:
            # 항목이 파일인 경우, 파일을 삭제
            os.remove(item_path)
            print(f"파일 삭제: {item_path}")

# 재귀 함수를 실행하여 'source' 폴더의 내용을 삭제
delete_contents_recursively('source')
# 마지막으로 'source' 폴더 자체를 삭제
os.rmdir('source')
print("재귀 함수를 통한 삭제 완료!")

# shutil.rmtree()를 사용해 폴더 내용 삭제
print("\n>>> shutil.rmtree()를 사용해 폴더 통째로 삭제하기")
# 다시 예제 실행을 위해 'source' 폴더 구조를 만들기
os.makedirs('source/test_folder1', exist_ok=True)
with open('source/test1.txt', 'w') as f:
    f.write('This file is shutil test file1.')
with open('source/test_folder1/test2.txt', 'w') as f:
    f.write('This file is shutil test file2.')
    
# shutil.rmtree()가 실행되기 전에 잠시 멈추는 부분
input("\n**폴더가 생성되었습니다. 삭제 전 폴더를 확인하려면 엔터를 누르세요.**\n")

try:
    source_dir = 'source'
    # shutil.rmtree()는 내부적으로 복잡한 재귀 과정을 처리하여,
    # 단 한 줄로 폴더와 그 하위의 모든 파일, 폴더를 한꺼번에 삭제
    shutil.rmtree(source_dir)
    print(f"'{source_dir}' 폴더와 그 내용이 삭제되었습니다.")
    
except OSError as e:
    # 삭제 중 권한 문제 등 오류가 발생하면 메시지를 출력
    print(f"오류: 폴더 삭제에 실패했습니다. {e}")

print("\n예제 실행 완료.\n")




