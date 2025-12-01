import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from available_functions import available_functions
from call_function import call_function

load_dotenv()


def main():
    print("Hello from helper-bot!")

    args = sys.argv[1:] #creats args var without call

    if not args: #checks if theirs arguments
        print("Error, please provide prompt.")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY") #imports api key
    client = genai.Client(api_key=api_key) #creates new instance of gemini with key

    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ] #saves user messages

    generate_content(client, messages) #calls to generate content

    
def generate_content(client, messages):
    
    max_iters = 20
    for i in range(0, max_iters):

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )
        

        verbose_flag = False
        if len(sys.argv) == 3 and sys.argv[2] == "--verbose": #checks for --verbose command
            verbose_flag = True

        if verbose_flag: #adds --verbose content
            print(f"User prompt: {messages}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates: #puts all the functions it wants to call into the array
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        if response.function_calls: #calls all the functions in the array
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose_flag)
                messages.append(result)
        else:
            #final agent text response
            print(response.text)
            return

        
        


if __name__ == "__main__":
    main()
