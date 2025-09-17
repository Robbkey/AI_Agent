import os
from google.genai import types

#chapter 3 lection 2 further comment later
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="The function should write the content to the given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
             "file": types.Schema(
                type=types.Type.STRING,
                description="A file that should be inside the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be writen to a given file",
            ),
        },
    ),
)

def write_file(working_directory, file, content):

    #getting the absolute pathes for both inputs
    file_path = os.path.abspath(f"{working_directory}/{file}")
    working_directory_path = os.path.abspath(working_directory)
    path = os.path.join(working_directory_path, file_path)

    #if dircetory is something like /bin
    if file.startswith("/"):
        return f'Result for {file} directory:\n Error: Cannot write to "{file}" as it is outside the permitted working directory'

    #checking if inside allowed directory
    if working_directory_path not in file_path:
        return f'Result for {file} directory:\n Error: Cannot write to "{file}" as it is outside the permitted working directory'
    
    #cheking if file isn't a directory
    if os.path.isdir(file_path):
        return f'Result for {file} directory:\n Error: File not found or is not a regular file: {file}'


    try:
        with open(file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file}" ({len(content)} characters written)'

    except Exception as e:
        return f"Result for {file} file:\n Error: {e}"