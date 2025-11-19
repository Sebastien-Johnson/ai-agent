import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from call_function import available_functions

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
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
)
    
    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose": #checks for --verbose command
        verbose_flag = True

    if response.function_calls:
        for call in response.function_calls:
            f"Calling function: {function_call_part.name}({function_call_part.args})"

    if verbose_flag: #adds --verbose content
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
