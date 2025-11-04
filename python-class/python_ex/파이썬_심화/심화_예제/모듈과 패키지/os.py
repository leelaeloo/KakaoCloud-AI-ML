import os

# 현재 작업 디렉터리
cwd = os.getcwd()
print(f"현재 디렉터리 : {cwd}")


os.chdir('../')


os.mkdir('os_test_folder')
# os.makedirs('path/to/test/folder', exist_ok=True)   
os.rmdir('os_test_folder')

files = os.listdir('.')
print(f"현재 디렉터리 파일/폴더 : {files}")

# 파일 경로 조직
path = os.path.join('folder', 'file.txt')
dirname = os.path.dirname(path)
basename = os.path.basename(path)
exists = os.path.exists(path)
is_file = os.path.isfile(path)
is_dir = os.path.isdir(path)



