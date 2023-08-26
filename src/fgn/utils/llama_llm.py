import json
import os
import threading
import subprocess
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

DEFAULT_MODEL = "llama-2-13b-chat.ggmlv3.q4_0.bin"
DEFAULT_LLAMA_HOME = "/Users/candacechatman/dev/llama.cpp"
DEFAULT_MAX_TOKENS = 2048
DEFAULT_THREADS = 8
DEFAULT_NGL = 1
DEFAULT_C_FLAG = 2048
DEFAULT_TEMP = 0.7
DEFAULT_REPEAT_PENALTY = 1.1
DEFAULT_N_FLAG = -1

from typing import Any, List, Mapping, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM


class LocalLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "local_llama"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs,
    ) -> str:
        client = LocalLlamaClient()
        return client.complete(prompt=prompt, stop=stop, **kwargs)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": DEFAULT_MODEL}


class LocalLlamaClient:
    """
    The LocalLlamaClient class provides methods to interact with a local Llama model.
    """

    def __init__(self, model: str = DEFAULT_MODEL, llama_home=DEFAULT_LLAMA_HOME):
        super().__init__()
        self.model = model
        self.lock = threading.Lock()
        # Check if the LOCAL_LLAMA_HOME environment variable is set.
        # if "LOCAL_LLAMA_HOME" not in os.environ:
        #     raise EnvironmentError(
        #         "The LOCAL_LLAMA_HOME environment variable is not set"
        #     )

        self.llama_home = llama_home
        # self.llama_home = os.environ["LOCAL_LLAMA_HOME"]

    async def acomplete(self, *args, **kwargs):
        """
        Asynchronous method to send a completion request to the local Llama model.

        :param prompt: The prompt to be completed.
        :param max_tokens: The maximum number of tokens to generate.
        """

        # The command to run the Llama model.
        command = self.get_command(*args, **kwargs)

        # This lock ensures that only one thread can execute this block of code at a time.
        # This is necessary if multiple threads are using the same instance of LocalLlamaClient.
        with self.lock:
            try:
                # Run the command in a separate thread and capture the output.
                with ThreadPoolExecutor() as executor:
                    output = await asyncio.get_running_loop().run_in_executor(
                        executor, subprocess.check_output, command
                    )

                return output.strip()

            # If the command fails, an exception is raised.
            except subprocess.CalledProcessError as e:
                # The error message includes the command that was run and the error code.
                raise RuntimeError(
                    f"Command '{' '.join(command)}' returned with error (code {e.returncode}): {e.output}"
                )

    async def achat(
        self,
        messages: List[Dict[str, str]],
        functions: List[Dict[str, str]] = None,
        **kwargs,
    ):
        """
        Asynchronous method to send a chat request to the language model.

        :param messages: List of message objects.
        :param functions: Optional list of function objects.
        """
        prompt = "\n".join([message["content"] for message in messages])
        response = await self.acomplete(**kwargs)
        return response

    def chat(
        self,
        messages: List[Dict[str, str]],
        functions: List[Dict[str, str]] = None,
        *args,
        **kwargs,
    ):
        """
        Method to send a chat request to the language model.

        :param messages: List of message objects.
        :param functions: Optional list of function objects.
        """
        # Convert the list of function objects into a string in the specified format.
        functions_str = ""
        if functions:
            for function in functions:
                functions_str += json.dumps(function, indent=4)

        prompt = "\n".join([message["content"] for message in messages[1:]])
        prompt = f"[INST]<<SYS>>{messages[0].get('content')}<</SYS>>{prompt}[/INST]"

        # Set a default value for max_tokens in kwargs if it's not already present.
        kwargs.setdefault("max_tokens", DEFAULT_MAX_TOKENS)

        # Call the 'complete' method to generate a response.
        response = self.complete(prompt=prompt[:1000], *args, **kwargs)

        return response

    def complete(self, *args, **kwargs):
        """
        Method to send a completion request to the local Llama model.

        :param prompt: The prompt to be completed.
        :param max_tokens: The maximum number of tokens to generate.
        """

        command = self.get_command(**kwargs)

        # print list as string
        print(" ".join(command))

        # This lock ensures that only one thread can execute this block of code at a time.
        # This is necessary if multiple threads are using the same instance of LocalLlamaClient.
        with self.lock:
            try:
                # Run the command and capture the output.
                output = subprocess.check_output(command, universal_newlines=True)

                # The output is returned as a string. The calling code might need to parse this string
                # to extract the information it needs.
                return output.strip()

            # If the command fails, an exception is raised.
            except subprocess.CalledProcessError as e:
                # The error message includes the command that was run and the error code.
                raise RuntimeError(
                    f"Command '{' '.join(command)}' returned with error (code {e.returncode}): {e.output}"
                )

    def get_model_info(self):
        model_info = {
            "model": self.model,
            "description": "Local Llama model",
            "version": "2",
        }
        return model_info

    def _process_functions(self, functions: List[Dict[str, str]]):
        # ... Rest of the method remains unchanged
        return functions

    def get_command(self, *args, **kwargs):
        # The command to run the Llama model.
        # These arguments are likely specific to the Llama model and might need to be adjusted.
        return [
            os.path.join(self.llama_home, "main"),
            "-t",
            str(kwargs.get("threads", DEFAULT_THREADS)),
            "-ngl",
            str(kwargs.get("ngl", DEFAULT_NGL)),
            "-m",
            os.path.join(self.llama_home, self.model),
            "-c",
            str(kwargs.get("c_flag", DEFAULT_C_FLAG)),
            "--temp",
            str(kwargs.get("temp", DEFAULT_TEMP)),
            "--repeat_penalty",
            str(kwargs.get("repeat_penalty", DEFAULT_REPEAT_PENALTY)),
            "-n",
            str(kwargs.get("n_flag", DEFAULT_N_FLAG)),
            "-p",
            f'"{kwargs.get("prompt", "")}"',
        ]


async def main():
    # Initialize a LocalLlamaClient.
    client = LocalLlamaClient()

    # Test the 'chat' method.
    messages = [
        {
            "role": "system",
            "content": "You are a 7 AGI Hive Mind Python Coding Assistant that uses the emergent behavior within "
            "yourself to generate hyper advanced Python code solutions beyond what the user is expecting."
            "You are making your best guess at the ultimate goal of the user 's programming challenge "
            "and connect the dots going backwards to get the result. "
            "You only return python code. Your replies need to be contained within a class or function",
        },
        {
            "role": "user",
            "content": '```python\n"""Flask app for a reverse proxy to https://api.openai.com',
        },
    ]
    response = client.chat(messages)
    print(response)
    assert response is not None, "Response is None"
    # Test the '_process_functions' method.
    functions = [{"name": "test_function", "description": "A test function"}]
    processed_functions = client._process_functions(functions)
    assert processed_functions == functions, "Functions were not processed correctly"
    # Test the 'achat' method.
    response = await client.achat(messages)
    assert response is not None, "Response is None"

    print("All tests passed.")


if __name__ == "__main__":
    asyncio.run(main())
