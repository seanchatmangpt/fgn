import asyncio
import json
import os
from dataclasses import dataclass
from time import sleep
from typing import Union

import openai
from loguru import logger

from fgn.completion.prompt_schemas import *
from fgn.utils.llm_operations import generate_filename
from local_llama_client import LocalLlamaClient

DEFAULT_PROMPT = ""
DEFAULT_SYS_MSG = "A LLM 7 AGI Hive-Mind simulator"
DEFAULT_MODEL = "4"
DEFAULT_MAX_RETRY = 5
DEFAULT_BACKOFF_FACTOR = 2
DEFAULT_INITIAL_WAIT = .25


def chat(
        prompt=DEFAULT_PROMPT,
        sys_msg=DEFAULT_SYS_MSG,
        msgs=None,
        funcs=None,
        model=DEFAULT_MODEL,
        max_retry=DEFAULT_MAX_RETRY,
        backoff_factor=DEFAULT_BACKOFF_FACTOR,
        initial_wait=DEFAULT_INITIAL_WAIT,
        raw_msg=False,
        write_path=None,
        mode="a+"
) -> Union[str, dict]:
    """
    Customized completion function that interacts with the OpenAI API, capable of handling prompts, system messages,
    and specific functions. If the content length is too long, it will shorten the content and retry.

    Parameters:
        prompt (str, optional): The initial prompt for the chat conversation.
        sys_msg (str, optional): System message to guide the model's behavior.
        msgs (List[dict], optional): Previous messages in the conversation.
        funcs (List[Callable], optional): Custom functions to be applied on the response.
        model (str, optional): The OpenAI model to be used for completion.
        max_retry (int, optional): Maximum number of retries in case of an error.
        backoff_factor (float, optional): Multiplicative factor for exponential backoff between retries.
        initial_wait (float, optional): Initial wait time for the exponential backoff.
        raw_msg (bool, optional): Whether to include raw message in the response.
        write_path (str, optional): Directory or file path to write the response.
        mode (str, optional): File opening mode if writing response to file.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = _create_messages(sys_msg, prompt, msgs)

    retry = 0

    while retry <= max_retry:
        try:
            params = _create_params(model, messages, funcs)
            res = None

            if str(model) == "2":
                llama = LocalLlamaClient()
                res = llama.complete(prompt=prompt)
            elif funcs:
                res = get_response(
                    openai.ChatCompletion.create(**params), raw_msg=raw_msg, funcs=funcs
                )
            else:
                res = get_response(
                    openai.ChatCompletion.create(**params), raw_msg=raw_msg, funcs=funcs
                )

            if os.path.isdir(write_path):
                name = generate_filename(prompt)
                logger.info(f"Creating file {name} in {write_path}")
                write_path = os.path.join(write_path, generate_filename(prompt))
            if write_path:
                with open(write_path, mode) as f:
                    f.write(f"{res}\n")

            return res
        except Exception as oops:
            logger.warning(oops)
            # If the error is due to maximum context length, chop the messages and retry
            if "maximum context length" in str(oops):
                messages = messages[:1] + messages[2:]
                # Reset the retry attempts
                retry = 0
                continue

            # Increment the retry attempts
            retry += 1

            # If reached the maximum retry attempts, return the error message
            if retry > max_retry:
                raise ValueError(f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}")

            # Calculate the waiting time for exponential backoff
            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            # Print the error and wait before retrying
            logger.warning(
                f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
            )
            sleep(wait_time)


# Callable class version of chat using dataclass
@dataclass
class Chat:
    prompt = DEFAULT_PROMPT
    sys_msg = DEFAULT_SYS_MSG
    msgs = None
    funcs = None
    model = DEFAULT_MODEL
    max_retry = DEFAULT_MAX_RETRY
    backoff_factor = DEFAULT_BACKOFF_FACTOR
    initial_wait = DEFAULT_INITIAL_WAIT
    raw_msg = False

    def __call__(self):
        return chat(
            prompt=self.prompt,
            sys_msg=self.sys_msg,
            msgs=self.msgs,
            funcs=self.funcs,
            model=self.model,
            max_retry=self.max_retry,
            backoff_factor=self.backoff_factor,
            initial_wait=self.initial_wait,
            raw_msg=self.raw_msg,
        )

    def achat(self, *args, **kwargs):
        return achat(*args, **kwargs)


async def achat(
        prompt=DEFAULT_PROMPT,
        sys_msg=DEFAULT_SYS_MSG,
        msgs=None,
        funcs=None,
        model=DEFAULT_MODEL,
        max_retry=DEFAULT_MAX_RETRY,
        backoff_factor=DEFAULT_BACKOFF_FACTOR,
        initial_wait=DEFAULT_INITIAL_WAIT,
        raw_msg=False,
) -> Union[str, dict]:
    """
    Customized completion function that interacts with the OpenAI API, capable of handling prompts, system messages,
    and specific functions. If the content length is too long, it will shorten the content and retry.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = _create_messages(sys_msg, prompt, msgs)

    if funcs is None:
        funcs = []

    # Initialize retry attempts
    retry = 0

    # Run the loop for retry attempts
    while retry <= max_retry:
        try:
            params = _create_params(model, messages, funcs)

            if funcs:
                return get_response(
                    await openai.ChatCompletion.acreate(**params), raw_msg=raw_msg, funcs=funcs
                )
            else:
                return get_response(
                    await openai.ChatCompletion.acreate(**params), raw_msg=raw_msg, funcs=funcs
                )
        except Exception as oops:
            logger.warning(oops)
            # If the error is due to maximum context length, chop the messages and retry
            if "maximum context length" in str(oops):
                messages = messages[:1] + messages[2:]
                # Reset the retry attempts
                retry = 0
                continue

            retry += 1

            if retry > max_retry:
                raise ValueError(f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}")

            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            print(
                f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
            )
            await asyncio.sleep(wait_time)


def get_response(res, raw_msg, funcs):
    msg = res.get("choices")[0].get("message")

    if raw_msg:
        return msg

    func = msg.get("function_call")

    if func:
        try:
            func["arguments"] = json.loads(func.get("arguments", ""))
        except json.decoder.JSONDecodeError:
            pass
        # if it is not a valid json, {"name": "func_name", "arguments": {}}, throw a error
        if not isinstance(func, dict) or not isinstance(func.get("arguments"), dict):
            error_msg = f"Invalid function response from OpenAI API {msg}"
            logger.exception(error_msg)
            raise ValueError(error_msg)
        else:
            return func
    elif len(funcs) > 0:
        error_msg = f"Invalid function response from OpenAI API {msg}"
        logger.exception(error_msg)
        raise ValueError(error_msg)
    else:
        return msg.get("content", "").strip()


def get_model_str(model):
    if model == "3":
        return "gpt-3.5-turbo-0613"
    elif model == "4":
        return "gpt-4-0613"
    else:
        return model


def _create_params(model, messages, funcs=None):
    parameters = {
        "model": get_model_str(model),
        "messages": messages,
    }
    if funcs:
        parameters["functions"] = funcs
        parameters["function_call"] = "auto"

    return parameters


def _create_messages(prompt, sys_msg, msgs):
    messages = []

    if msgs is None:
        messages = [
            {"role": "system", "content": sys_msg},
        ]

    if prompt:
        messages.append({"role": "user", "content": prompt})

    # Extend the messages list with the provided prompt, system message, and previous messages
    if msgs:
        messages.extend(msgs)

    return messages


def shell_command():
    # Step 1: send the conversation and available functions to GPT
    messages = [
        msg_schema(
            "What is the shell command to create a python project with pyscaffold?"
        )
    ]
    functions = [
        str_func_schema(
            "execute_shell",
            "A shell command to execute in one line. No explanation or description needed.",
            "command",
            "The shell command to execute in one line. No explanation or description needed.",
        ),
    ]
    response = chat(
        prompt="",
        sys_msg="A LLM 7 AGI Hive-Mind simulator that can only return three lines of text in ```shell``` mode."
                "You do not provide explanations or any other information, just the three lines of text.",
        msgs=messages,
        funcs=functions,
        model="3",
        # raw_msg=True,
    )

    print(response)


code = '''
from dataclasses import dataclass
from typing import List

from gen_entities import generate_reporting_system_entities
from gen_web_crud import generate_web_crud
from typetemp.template.typed_template import TypedTemplate
from typetemp.utils import create_init_files


@dataclass
class FlaskAppTemplate(TypedTemplate):
    entities: List[str] = None
    to: str = "./app.py"
    source = """
from flask import Flask, render_template
{% for entity in entities %}
from web.routes.{{ entity }}Routes import app as {{ entity.lower() }}_app
{% endfor %}

app = Flask(__name__)

{% for entity in entities %}
app.register_blueprint({{ entity.lower() }}_app, url_prefix='/{{ entity.lower() }}')
{% endfor %}

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    """


def generate_app():
    entities = ['Email', 'Employee', 'Feedback', 'Report']

    generate_reporting_system_entities(entities)

    # Generate web CRUD interfaces
    generate_web_crud(entities)

    # Create Flask App using the defined entities
    flask_app_template = FlaskAppTemplate(entities=entities)
    flask_app_template.render()

    create_init_files()

    print("Flask app generated successfully.")


# Run the function to generate the Flask app
generate_app()

 '''

if __name__ == "__main__":
    # shell_command()
    i = 0
    while True:
        chat(model="2", write_path=f"output{i}.py", prompt=code + "\n\n ### The most overengineered example possible\n\n\\\\python```python\nclass")
