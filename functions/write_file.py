import os

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