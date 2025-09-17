import os
import subprocess
from google.genai import types

#chapter 3 lection 2 further comment later
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specific given python script, with the option of giving arguments to the script.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="A file that should be inside the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="A list of optional arguments for the file",
            ),
        },
    ),
)

def run_python_file(working_directory, file, args=[]):

     #getting the absolute pathes for both inputs
    file_path = os.path.abspath(f"{working_directory}/{file}")
    working_directory_path = os.path.abspath(working_directory)
    path = os.path.join(working_directory_path, file_path)

    #if dircetory is something like /bin
    if file.startswith("/"):
        return f'Result for {file} directory:\n Error: Cannot execute "{file}" as it is outside the permitted working directory'

    #checking if inside allowed directory
    if working_directory_path not in file_path:
        return f'Result for {file} directory:\n Error: Cannot execute "{file}" as it is outside the permitted working directory'
    
    #cheking if file isn't a directory
    if file[-3:] != ".py":
        return f'Result for {file} directory:\n Error: "{file}" is not a Python file.'

    if file not in os.listdir(working_directory_path):
        return f'Error: File "{file}" not found.'

    try:
        result = subprocess.run(
            ["python3", file_path, *args], 
            timeout=30, 
            capture_output=True, 
            cwd=working_directory_path, 
            text=True,
            )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."

    except FileNotFoundError:
        return f'Result for {file} directory:\n Error: "{file}" is not a Python file.'
    except Exception as e:
        return f"Error: executing Python file: {e}"
