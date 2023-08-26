import json
import logging

import pytest
from unittest.mock import patch
from faker import Faker
import requests_mock
import os


from fgn.utils.llm_operations import chat

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
                        "args": {"props": [{"key": fake.word(), "value": fake.word()}]},
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


# Define the custom function as per the OpenAI docs
get_current_weather_function = {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
}

weather_api_response = {"temperature": 22, "unit": "celsius", "description": "Sunny"}


def mock_openai_weather_request():
    return {
        "id": "chatcmpl-123",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": "get_current_weather",
                        "arguments": {"location": "Boston, MA"},
                    },
                },
                "finish_reason": "function_call",
            }
        ],
    }


def mock_openai_weather_request_second():
    return {
        "id": "chatcmpl-123",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "The weather in Boston is currently sunny with a temperature of 22 degrees Celsius.",
                },
                "finish_reason": "stop",
            }
        ],
    }


def test_openai_weather_interaction():
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

    prompt = "What is the weather like in Boston?"

    first_openai_response = mock_openai_weather_request()
    second_openai_response = mock_openai_weather_request_second()

    with requests_mock.Mocker() as m:
        m.get("https://weatherapi.com/", text=json.dumps(weather_api_response))

        with patch("openai.ChatCompletion.create") as mock_create:
            mock_create.side_effect = [first_openai_response, second_openai_response]

            result = chat(prompt, funcs=[get_current_weather_function])

            assert result == {
                "name": "get_current_weather",
                "arguments": {"location": "Boston, MA"},
            }

            # Call complete function with updated messages
            updated_prompt = [
                {"role": "user", "content": prompt},
                {
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": "get_current_weather",
                        "arguments": {"location": "Boston, MA"},
                    },
                },
                {
                    "role": "function",
                    "name": "get_current_weather",
                    "content": weather_api_response,
                },
            ]
            final_result = chat(
                msgs=updated_prompt, funcs=[get_current_weather_function]
            )

            assert (
                final_result
                == "The weather in Boston is currently sunny with a temperature of 22 degrees Celsius."
            )
