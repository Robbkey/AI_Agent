import os
from google.genai import types

#chapter 3 lection 2 further comment later
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    #if dircetory is something like /bin
    if directory.startswith("/"):
        return f'Result for {directory} directory:\n Error: Cannot list "{directory}" as it is outside the permitted working directory'

    #getting the absolute pathes for both inputs
    directory_path = os.path.abspath(f"{working_directory}/{directory}")
    working_directory_path = os.path.abspath(working_directory)
    path = os.path.join(working_directory_path, directory_path)

    #checking if inside allowed directory
    if working_directory_path not in directory_path:
        return f'Result for {directory} directory:\n Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    #cheking if directory isn't a file
    if os.path.isfile(directory_path):
        return f'Result for {directory} directory:\n Error: "{directory}" is not a directory'

    #error handle
    try:
        #getting the content of a directory
        conten_list = os.listdir(path)
        #creating a function for mapping that creats a string with file infos
        func = lambda x: f" - {x}:file_size={os.path.getsize(os.path.join(path, x))} bytes, is_dir={os.path.isdir(os.path.join(path, x))}"

        #joining all stings into a multiline string
        full_string ="\n".join(list(map(func,conten_list)))
        #output formating
        if directory == ".":
            final_string = f"Result for current directory:\n{full_string}"
        else:
            final_string = f"Result for {directory} directory:\n{full_string}"
        return final_string

    #error return
    except Exception as e:
        return f"Result for {directory} directory:\n Error: {e}"


#test case for running the script
if __name__ == "__get_file_info__":
    get_files_info("/home/robbkey/Desktop/BootDev/github.com/Robbkey/AI_Agent/calculator/", "../")