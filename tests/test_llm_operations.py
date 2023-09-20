import json
import logging

import pytest
from unittest.mock import patch
from faker import Faker
import requests_mock
import os


import asyncio
import json
import os
from time import sleep
from typing import Union

import openai
from loguru import logger


def chat(
    prompt="",
    sys_msg="A LLM 7 AGI Hive-Mind simulator",
    msgs=None,
    funcs=None,
    model="gpt-3.5-turbo-0613",
    max_retry=1,
    backoff_factor=2,
    initial_wait=0.25,
) -> Union[str, dict]:
    """
    Customized completion function that interacts with the OpenAI API, capable of handling prompts, system messages,
    and specific functions. If the content length is too long, it will shorten the content and retry.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if msgs is None:
        msgs = []

    # Extend the messages list with the provided prompt, system message, and previous messages
    messages = [
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": prompt},
    ]
    messages.extend(msgs)

    # Initialize retry attempts
    retry = 0

    # Run the loop for retry attempts
    while retry <= max_retry:
        try:
            response = None

            if funcs:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    functions=funcs,
                    function_call="auto",
                )
            else:
                response = openai.ChatCompletion.create(model=model, messages=messages)
            function_call = (
                response.get("choices", [{}])[0].get("message", {}).get("function_call")
            )
            if function_call:
                print("WTF???", function_call)
                function_call["arguments"] = json.loads(
                    function_call.get("arguments", "")
                )
                return function_call
            else:
                return response["choices"][0]["message"]["content"].strip()
        except Exception as oops:
            logger.warn(oops)
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
                return str(oops)

            # Calculate the waiting time for exponential backoff
            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            # Print the error and wait before retrying
            logger.warn(
                f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
            )
            sleep(wait_time)


# Configure logging
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def mock_openai_create():
    with patch("fgn.utils.llm_operations.openai.ChatCompletion.create") as mock_create:
        mock_create.side_effect = lambda *args, **kwargs: logging.debug(
            f"Mock OpenAI called with args: {args}, kwargs: {kwargs}"
        ) or {"choices": [{"message": {"content": "success"}}]}
        yield mock_create


# Successful response
def mock_openai_create_success(*args, **kwargs):
    logging.debug(f"Mock OpenAI called with args: {args}, kwargs: {kwargs}")
    return {"choices": [{"message": {"content": "success"}}]}


@pytest.mark.parametrize(
    "create_mock,expected",
    [
        (mock_openai_create_success, "success"),
    ],
)
def test_complete_success(create_mock, expected):
    with patch("fgn.utils.llm_operations.openai.ChatCompletion.create", create_mock):
        result = chat("prompt")
        assert result == "success"


def test_complete_with_functions():
    # Define a mock OpenAI response
    response = {"choices": [{"message": {"content": "success"}}]}

    # Patch the OpenAI API call to return the mock response
    with patch("fgn.utils.llm_operations.openai.ChatCompletion.create") as mock_create:
        mock_create.return_value = response

        # Define a custom function with specific arguments
        custom_function = {
            "name": "example_function",
            "args": {"delete_me": "This will be removed"},
        }

        # Invoke the complete method with the custom function
        result = chat("prompt", funcs=[custom_function])

        # Assert that the result is as expected
        assert result == "success"

        # Retrieve the function call from the mocked OpenAI API call
        function_call_sent = mock_create.call_args.kwargs["functions"]

        # Assert that the custom function has been passed correctly
        assert function_call_sent == [custom_function]


fake = Faker()


# AGI 1: "Let's ensure that the function name and parameters are matched exactly as expected in the response."
def mock_change_value_response(*args, **kwargs):
    return {
        "choices": [
            {
                "message": {
                    "content": fake.sentence(),
                    "function_call": {
                        "name": "change_value",
                        "arguments": json.dumps(
                            {"props": [{"key": fake.word(), "value": fake.word()}]}
                        ),
                    },
                }
            }
        ]
    }


# AGI 2: "Consider defining the custom function outside the test to avoid redundancy. It will make the test cleaner."
change_value_function = {
    "name": "change_value",
    "description": "Update value of object key",
    "parameters": {
        "type": "object",
        "properties": {
            "props": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "description": fake.sentence()},
                        "value": {"type": "string", "description": fake.sentence()},
                    },
                },
            }
        },
        "required": ["props"],
    },
}


def test_complete_with_functions2():
    prompt = "Change the text to Hello World and top to 10 and left to 30"

    with patch(
        "fgn.utils.llm_operations.openai.ChatCompletion.create",
        new=mock_change_value_response,
    ):
        result = chat(prompt, funcs=[change_value_function])
        assert isinstance(result, dict)
