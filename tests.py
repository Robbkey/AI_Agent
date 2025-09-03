'''
test case for get_files_info
from functions.get_files_info import get_files_info

test1 = get_files_info("calculator", ".")
print(test1)

test2 = get_files_info("calculator", "pkg")
print(test2)

test3 = get_files_info("calculator", "/bin")
print(test3)

test4 = get_files_info("calculator", "../")
print(test4)
'''

'''
test for get_files_content
from functions.get_files_content import get_files_content

test1 = get_files_content("calculator", "main.py")
print(f"this is the lenght: {len(test1)}")
print("this is the content:")
print(test1)

test2 = get_files_content("calculator", "pkg/calculator.py")
print(f"this is the lenght: {len(test2)}")
print("this is the content:")
print(test2)

test3 = get_files_content("calculator", "/bin/cat")
print(f"this is the lenght: {len(test3)}")
print("this is the content:")
print(test3)

test4 = get_files_content("calculator", "pkg/does_not_exist.py")
print(f"this is the lenght: {len(test4)}")
print("this is the content:")
print(test4)
'''