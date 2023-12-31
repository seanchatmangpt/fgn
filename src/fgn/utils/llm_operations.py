import asyncio
import json
import os
import re
import uuid
from time import gmtime, sleep, strftime
from typing import Union

import openai
from loguru import logger
from rich import print

from fgn.utils.file_operations import open_file, save_to_project_folder

from .llama_llm import LocalLlamaClient

openai.api_key = os.environ["OPENAI_API_KEY"]


def save_completion(prompt):
    zulu = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    save_to_project_folder(
        f"data/completion/completion_{uuid.uuid4()}_{zulu}.txt", prompt
    )


def save_embedding(prompt):
    zulu = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    save_to_project_folder(
        f"data/embeddings/embedding_{uuid.uuid4()}_{zulu}.txt", prompt
    )


def gpt3_completion(
    prompt,
    engine="text-davinci-003",
    temp=1.0,
    top_p=1.0,
    tokens=400,
    freq_pen=0.0,
    pres_pen=0.0,
    stop=None,
):
    if stop is None:
        stop = ["<<STOP>>"]
    max_retry = 3
    retry = 0
    prompt = prompt.encode(encoding="ASCII", errors="ignore").decode()
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop,
            )
            text = response["choices"][0]["text"].strip()
            save_completion(text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print("Error communicating with OpenAI:", oops)
            sleep(1)


def gpt_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    emb = openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]
    save_embedding(emb)
    return emb


def gpt_chat_completion(
    messages, model, max_retry=5, backoff_factor=2, initial_wait=0.1
):
    """
    Sends chat inputs to OpenAI API and receives the chatbot response.

    Args:
        messages (List[Dict]): A list of messages with role and content.
        model (str, optional): The GPT model to be used.
        max_retry (int, optional): The maximum number of retries.
        backoff_factor (int, optional): The factor to exponentially increase the waiting time.
        initial_wait (float, optional): The initial waiting time between retries in seconds.

    Returns:
        str: The content of the message generated by the chatbot.
    """

    # Initialize retry attempts
    retry = 0

    # Run the loop for retry attempts
    while retry <= max_retry:
        try:
            if model == "2":
                llama = LocalLlamaClient()
                response = llama.chat(messages)
                save_completion(response)
                return response
            response = openai.ChatCompletion.create(model=model, messages=messages)
            text = response["choices"][0]["message"]["content"].strip()
            save_completion(text)
            return text
        except Exception as oops:
            # If the error is due to maximum context length, return the error message so that the user can handle it
            if "maximum context length" in str(oops):
                return f"GPT error: {oops}"

            retry += 1  # Increment the retry attempts

            # If reached the maximum retry attempts, return the error message
            if retry > max_retry:
                return f"GPT error: {oops}"

            # Calculate the waiting time for exponential backoff
            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            # Print the error and wait before retrying
            print(
                f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
            )
            sleep(wait_time)


def gpt4_completion(prompt, model="gpt-4"):
    completion = gpt_chat_completion([{"role": "user", "content": prompt}], model=model)
    save_completion(completion)
    return completion


def generate_filename(
    prompt, prefix="", suffix="", extension="md", max_chars=60, time=False
):
    """
    Generates a filename based on the given prompt.
    :param prompt: the prompt to generate the filename from
    :param prefix: the prefix to add to the filename
    :param suffix: the suffix to add to the filename
    :param extension: the extension to add to the filename
    :param max_chars: the maximum number of characters in the filename (default: 60)
    :param time: whether to add the current time to the filename (default: False)
    :return: the generated filename
    """
    prompt = prompt[:300]

    file_name = gpt3_completion(
        f"Carefully read the following text and generate a highly relevant and unique filename for it. The filename "
        f"should be in all lowercase letters and consist of at most {max_chars} characters, separated by underscores. "
        f"Exclude any file extensions from the filename. Pay close attention to the content "
        f"and context of the text to avoid hallucinations or mistakes. The text is: '{prompt}'\n\nfile name:",
        temp=0,
        tokens=max_chars * 10,
    )

    # Remove all non-underscore and non-alphanumeric characters, and truncate to max_chars
    file_name = re.sub(r"[^a-zA-Z0-9_]", "", file_name)
    file_name = file_name[:max_chars]

    if prefix:
        file_name = f"{prefix}_{file_name}"

    if suffix:
        file_name = f"{file_name}_{suffix}"

    if time:
        file_name = f"{file_name}_{strftime('%Y-%m-%d_%H-%M-%S', gmtime())}"

    if extension:
        file_name = f"{file_name}.{extension}"

    # print('Generated filename:', file_name)

    return file_name


def generate_output_file(prompt, extension="md", max_chars=60, time=True):
    return generate_filename(
        prompt, extension=extension, max_chars=max_chars, time=time
    )


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


async def achat(
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

    if funcs is None:
        funcs = []

    # Initialize retry attempts
    retry = 0

    # Run the loop for retry attempts
    while retry <= max_retry:
        try:
            response = None

            if funcs:
                response = await openai.ChatCompletion.acreate(
                    model=model,
                    messages=messages,
                    functions=funcs,
                    function_call="auto",
                )
            else:
                response = await openai.ChatCompletion.acreate(
                    model=model, messages=messages
                )
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
                return f"GPT error: {oops}"

            # Calculate the waiting time for exponential backoff
            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            # Print the error and wait before retrying
            print(
                f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}"
            )
            sleep(wait_time)
