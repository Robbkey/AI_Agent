# to run the script over the command line use the following command
# uv run main.py "your llm prompt" other flags

import os #import so that the script can work in the os
import sys
from dotenv import load_dotenv #command for loading the .env file inside the main directory, so that the api key is usable 
from google import genai
from google.genai import types


def main():
    load_dotenv() # loading the .env file
    api_key = os.environ.get("GEMINI_API_KEY") # saving the api key
    client = genai.Client(api_key=api_key) # saving an instance of gemini with the api key 

    system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'" #system prompt to give overall instruction on how the llm should answer
    

    if len(sys.argv) > 1: # checking if a user input was given
        user_prompt = sys.argv[1] # saving the message part inside user_prompt. argv[0] is the filename
        messages = [
            types.Content(role="user", parts=[types.Part (text=user_prompt)]),
        ] # giving the user a role for later message history
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        ) # saving the llm respons and declaring which model to use, config to give the llm a system prompt to act on
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
    print("Response:")
    print(response.text)

# checking if the script is run with in it self or called by an other
if __name__ == "__main__":
    main()
