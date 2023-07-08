import requests
import logging
import traceback
import json
import sys
import os.path
from termcolor import colored

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if config.py exists
if not os.path.isfile('config.py'):
    # Prompt user for API key
    api_key = input("Enter your API key: ")

    # Create and populate config.py with the API key
    with open('config.py', 'w') as config_file:
        config_file.write(f"API_KEY = '{api_key}'")
else:
    # Load API key from config.py
    import config
    api_key = config.API_KEY

# Function to probe the endpoint and check its status
def probe_endpoint(endpoint):
    try:
        url = f"https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "test"}
            ],
            "model": endpoint,
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as error:
        return False
    except requests.exceptions.RequestException as error:
        return False

# Define available models and their corresponding endpoints
models = {
    'gpt-3.5-turbo': 'gpt-3.5-turbo',
    'gpt-3.5-turbo-0613': 'gpt-3.5-turbo-0613',
    'gpt-3.5-turbo-16k': 'gpt-3.5-turbo-16k',
    'gpt-3.5-turbo-16k-0613': 'gpt-3.5-turbo-16k-0613',
    'gpt-4': 'gpt-4',
    'gpt-4-0613': 'gpt-4-0613',
    'gpt-4-32k': 'gpt-4-32k',
    'gpt-4-32k-0613': 'gpt-4-32k-0613',
}

# Check if there's only one model defined
if len(models) == 1:
    chat_model = list(models.values())[0]
else:
    print("Available models:")
    default_model = 'gpt-3.5-turbo'
    for key, value in models.items():
        status = probe_endpoint(value)
        status_label = colored("*ACTIVE*", "green") if status else colored("*INACTIVE*", "red")
        default = "(Default)" if value == default_model else ""
        print(f"{value} {status_label} {default}")

    while True:
        selection = input("Select a model by entering its number: ")

        if selection.isdigit() and 1 <= int(selection) <= len(models):
            chat_model = list(models.values())[int(selection) - 1]
            break
        elif selection.strip() == "":
            chat_model = models[default_model]
            break
        else:
            print("Invalid selection. Please enter a valid number or leave it blank for the default model.")


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
        url = f"https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            "model": chat_model,
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        generated_message = response.json()['choices'][0]['message']['content']
        print("AI: ", generated_message)
        code_buffer.append(generated_message)
    except requests.exceptions.HTTPError as error:
        print("HTTP Error occurred:", error)
        traceback.print_exc()
    except requests.exceptions.RequestException as error:
        print("An error occurred:", error)
        traceback.print_exc()
