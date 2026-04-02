import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("invalid api key!")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

for _ in range(20):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("invalid usage metadata")

    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Add model's candidates to conversation history
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # Check if model wants to call functions
    if response.function_calls:
        function_responses = []
        for func in response.function_calls:
            function_call_result = call_function(func, verbose=args.verbose)

            if not function_call_result.parts:
                raise Exception("empty parts from function_call_result")

            if not function_call_result.parts[0].function_response:
                raise Exception("invalid function_call_result.parts[0].function_response")

            if function_call_result.parts[0].function_response.response is None:
                raise Exception("invalid function_call_result.parts[0].function_response.response")

            function_responses.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        # Add function results to conversation history
        messages.append(types.Content(role="user", parts=function_responses))
    else:
        # No function calls - model has final response
        print("Final response:")
        print(response.text)
        break
else:
    # Loop completed without breaking - max iterations reached
    print("Error: Maximum iterations reached without final response")
    sys.exit(1)
