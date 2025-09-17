# to run the script over the command line use the following command
# uv run main.py "your llm prompt" other flags

import os #import so that the script can work in the os
import sys
from dotenv import load_dotenv #command for loading the .env file inside the main directory, so that the api key is usable 
from google import genai
from google.genai import types
#to import the schemas
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    load_dotenv() # loading the .env file
    api_key = os.environ.get("GEMINI_API_KEY") # saving the api key
    client = genai.Client(api_key=api_key) # saving an instance of gemini with the api key 

#-------------- 
#system prompt to give overall instruction on how the llm should answer
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
#-------------- 


    #giving the llm the information which functions are avaiable
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
    

    if len(sys.argv) > 1: # checking if a user input was given
        user_prompt = sys.argv[1] # saving the message part inside user_prompt. argv[0] is the filename
        messages = [
            types.Content(role="user", parts=[types.Part (text=user_prompt)]),
        ] # giving the user a role for later message history
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],system_instruction=system_prompt),
        ) # saving the llm respons and declaring which model to use, config to give the llm a system prompt to act on and tools like functions it can use

    else:
        sys.exit(1) # programm exit when no input message is given

    # general output, with input and output tokens
    if len(sys.argv) > 2:# more infos if the --verbose flag is given
        if sys.argv[2] == "--verbose":
            print(f"User prompt: {user_prompt}")
            print("----------------------------------")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("----------------------------------")

    #lookig if a function was called by the llm
    if len(response.function_calls) > 0 :
        #printing the input for each function
        for func in response.function_calls:
            print(f"Calling function: {func.name}({func.args})")

    #if no function was used just print the respons.text
    else:
        print("Response:")
        print(response.text)

# checking if the script is run with in it self or called by an other
if __name__ == "__main__":
    main()
