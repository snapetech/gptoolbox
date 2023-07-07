import requests
import logging
import traceback
import json
import sys

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set API key
api_key = config.API_KEY

# Set default chat model
chat_model = 'gpt-3.5-turbo-16k'

# Initialize an empty list to hold the code snippets
code_buffer = []

while True:
    user_input = input("You: ")

    # Check for exit command
    if user_input.lower() == 'exit':
        break

    # Check for switch command
    if user_input.lower().startswith('switch:'):
        _, model = user_input.split(':')
        model = model.strip()
        if model == chat_model:
            print(f"You are already using the {chat_model} model.")
        else:
            chat_model = model
            code_buffer = []  # Clear code buffer when switching models
            print(f"Switched to {chat_model} model.")
        continue

    # Check for save command
    if user_input.lower().startswith('save:'):
        if not code_buffer:
            print("There is no code to save.")
        else:
            file_name = user_input[5:].strip()  # Extract the file name from user input
            if file_name:
                with open(file_name, 'w') as f:
                    f.write(code_buffer[-1])  # Write the most recent code block
                print(f"Code saved as {file_name}")
            else:
                print("Invalid file name. Please provide a valid file name.")
        continue

    try:
        # Make request to GPT-3 and append the generated code to the code buffer
        url = f"https://api.openai.com/v1/engines/{chat_model}/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "prompt": user_input,
            "max_tokens": 100,
            "n": 1
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        generated_message = response.json()['choices'][0]['text']
        print("AI: ", generated_message)
        code_buffer.append(generated_message)
    except requests.exceptions.HTTPError as error:
        print("HTTP Error occurred:", error)
        traceback.print_exc()
    except requests.exceptions.RequestException as error:
        print("An error occurred:", error)
        traceback.print_exc()
