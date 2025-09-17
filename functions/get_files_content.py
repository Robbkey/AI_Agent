import os
from functions.config import CHARACTER_LIMIT
from google.genai import types

#chapter 3 lection 2 further comment later
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="returns the content of a given file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="A file that should be inside the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file):

    #getting the absolute pathes for both inputs
    file_path = os.path.abspath(f"{working_directory}/{file}")
    working_directory_path = os.path.abspath(working_directory)
    path = os.path.join(working_directory_path, file_path)

    #if dircetory is something like /bin
    if file.startswith("/"):
        return f'Result for {file} directory:\n Error: Cannot read {file} as it is outside the permitted working directory'

    #checking if inside allowed directory
    if working_directory_path not in file_path:
        return f'Result for {file} directory:\n Error: Error: Cannot read{file} as it is outside the permitted working directory'
    
    #cheking if file isn't a directory
    if os.path.isdir(file_path):
        return f'Result for {file} directory:\n Error: File not found or is not a regular file: {file}'

    try:
        #reading a file and saving it's conten to a variable
        with open(file_path, "r") as f:
            file_content_string = f.read(CHARACTER_LIMIT)
            return file_content_string
    except Exception as e:
        return f"Result for {file} file:\n Error: {e}"