import openai
import json


def hello_world_in_french():
    """
    Custom function to produce the French translation of 'Hello, world!'
    :return: The string 'Bonjour, monde!'
    """
    return 'Bonjour, monde!'


def build_chat_model():
    """
    Function to handle building the chat model and sending chat completion requests.
    This function uses a custom function via the funcs parameter.
    """
    # Store API Key
    openai.api_key = 'api_key'

    # Define the chat completion model
    model = "gpt-3.5-turbo"

    # Prepare system message
    system = "You are an AI language model with profound linguistic knowledge."

    # Prepare user message that calls the custom function
    user_call = "Translate the following English text to French: 'Hello, world!'"

    # Create a function to be able to call the custom function hello_world_in_french
    function_def = f"""
    def translate_to_french(text: str) -> str:
        if text.lower() == 'hello, world!':
            return {json.dumps(hello_world_in_french())}
        else:
            return ""
    """

    # JSON Array containing the messages
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": { "function": "translate_to_french", "arguments": {"text": "Hello, world!"} }},
    ]

    # Add function to the functions parameter
    funcs = [
        {
            "name": "translate_to_french",
            "code": function_def,
        },
    ]

    # Use OpenAI's `ChatCompletion` to generate a conversation based on the given messages, model, and functions
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=funcs,
    )

    # Print the assistant's message
    print(response['choices'][0]['message']['content'])


# Run the function
build_chat_model()
