import time
import openai
from typing import Optional, List, Dict, Any

class OpenAIChat:

    MAX_RETRIES = 3  # Maximum number of retries before considering the request failed

    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key

    def chat(self, prompt: str, model: str, tokens: int, funcs: Optional[List[dict]] = None) -> Any:
        """
        Send chat completion request to OpenAI API. 
        If an OpenAI Error occurs, it tries again for a maximum of `MAX_RETRIES` times.
        :param prompt: string, the conversation so far
        :param model: string, OpenAI Model ID
        :param tokens: integer, maximum number of tokens for the response
        :param funcs: list, the code functions for the chat models
        :return: chat model's assistant response
        """
        retries = self.MAX_RETRIES
        while retries > 0:
            try:
                # Send the request to OpenAI API
                response = openai.ChatCompletion.create(
                    model=model,
                    tokens=tokens,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    functions=funcs,
                )

                # Return the assistant's reply
                for message in reversed(response['choices'][0]['messages']):
                    if message['role'] == 'assistant':
                        return message['content']

            except openai.OpenAIError as e:
                print(f"OpenAIError occurred: {e}")
                # If there's an OpenAI error, wait for a second and then try again
                time.sleep(1)
                retries -= 1

        # If the code reaches here, it means all attempts have failed
        raise RuntimeError("All attempts to request OpenAI API failed")

              
if __name__ == "__main__":
    openai_chat = OpenAIChat(api_key="your-api-key-here")
    prompt = "How does the Python 'for' loop work?"
    model = "gpt-3.5-turbo"
    tokens = 500
    # Get the assistant's response
    response = openai_chat.chat(prompt, model, tokens)
    print(f"Assistant: {response}")
