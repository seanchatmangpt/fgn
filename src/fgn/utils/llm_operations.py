from __future__ import annotations

import asyncio
import json
import os
import re
import unicodedata
import uuid
from time import gmtime, sleep, strftime
from typing import Any, Iterable, Mapping, Sequence, Union

from fgn.utils.file_operations import save_to_project_folder


class LLMProviderError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _openai_client(client: Any = None) -> Any:
    if client is not None:
        return client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise LLMProviderError("OPENAI_API_KEY_MISSING", "OPENAI_API_KEY is required for OpenAI-backed generation")
    try:
        from openai import OpenAI
    except ImportError as error:
        raise LLMProviderError("OPENAI_SDK_MISSING", "Install the 'openai' package to use OpenAI-backed generation") from error
    return OpenAI(api_key=api_key)


def _async_openai_client(client: Any = None) -> Any:
    if client is not None:
        return client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise LLMProviderError("OPENAI_API_KEY_MISSING", "OPENAI_API_KEY is required for OpenAI-backed generation")
    try:
        from openai import AsyncOpenAI
    except ImportError as error:
        raise LLMProviderError("OPENAI_SDK_MISSING", "Install the 'openai' package to use OpenAI-backed generation") from error
    return AsyncOpenAI(api_key=api_key)


def _message_content(response: Any) -> str:
    try:
        content = response.choices[0].message.content
    except AttributeError:
        content = response["choices"][0]["message"]["content"]
    if content is None:
        raise LLMProviderError("EMPTY_RESPONSE", "The provider returned no message content")
    return str(content).strip()


def _function_call(response: Any) -> Any:
    try:
        return response.choices[0].message.function_call
    except AttributeError:
        return response.get("choices", [{}])[0].get("message", {}).get("function_call")


def save_completion(content: str):
    zulu = strftime("%Y%m%dT%H%M%SZ", gmtime())
    return save_to_project_folder(f"data/completion/completion_{uuid.uuid4()}_{zulu}.txt", content)


def save_embedding(embedding: Sequence[float]):
    zulu = strftime("%Y%m%dT%H%M%SZ", gmtime())
    return save_to_project_folder(
        f"data/embeddings/embedding_{uuid.uuid4()}_{zulu}.json",
        json.dumps(list(embedding)),
    )


def gpt_chat_completion(
    messages: Iterable[Mapping[str, str]],
    model: str,
    max_retry: int = 5,
    backoff_factor: float = 2,
    initial_wait: float = 0.1,
    *,
    client: Any = None,
    sleep_fn=sleep,
) -> str:
    if model == "2":
        try:
            from .llama_llm import LocalLlamaClient
        except ImportError as error:
            raise LLMProviderError("LOCAL_PROVIDER_MISSING", "The local Llama provider is unavailable") from error
        response = LocalLlamaClient().chat(list(messages))
        save_completion(response)
        return response

    provider = _openai_client(client)
    message_list = list(messages)
    attempts = 0
    while True:
        try:
            response = provider.chat.completions.create(model=model, messages=message_list)
            text = _message_content(response)
            save_completion(text)
            return text
        except LLMProviderError:
            raise
        except Exception as error:
            if "maximum context length" in str(error).lower() or "context_length" in str(error).lower():
                raise LLMProviderError("CONTEXT_LENGTH_EXCEEDED", str(error)) from error
            attempts += 1
            if attempts > max_retry:
                raise LLMProviderError("PROVIDER_REQUEST_FAILED", str(error)) from error
            sleep_fn(initial_wait * (backoff_factor ** (attempts - 1)))


def gpt3_completion(
    prompt: str,
    engine: str = "text-davinci-003",
    temp: float = 1.0,
    top_p: float = 1.0,
    tokens: int = 400,
    freq_pen: float = 0.0,
    pres_pen: float = 0.0,
    stop=None,
    *,
    client: Any = None,
) -> str:
    del engine, temp, top_p, tokens, freq_pen, pres_pen, stop
    model = os.getenv("FGN_MODEL", "gpt-4o-mini")
    return gpt_chat_completion([{"role": "user", "content": prompt}], model=model, client=client)


def gpt4_completion(
    prompt: str,
    *,
    client: Any = None,
    model: str | None = None,
) -> str:
    """Compatibility entrypoint backed by the admitted modern chat client."""
    selected_model = model or os.getenv("FGN_MODEL", "gpt-4o-mini")
    return gpt_chat_completion(
        [{"role": "user", "content": prompt}],
        model=selected_model,
        client=client,
    )


def gpt_embedding(text: str, model: str = "text-embedding-3-small", *, client: Any = None):
    provider = _openai_client(client)
    response = provider.embeddings.create(input=[text.replace("\n", " ")], model=model)
    try:
        embedding = response.data[0].embedding
    except AttributeError:
        embedding = response["data"][0]["embedding"]
    save_embedding(embedding)
    return embedding


def generate_filename(prompt: str, prefix: str = "", suffix: str = "", extension: str = "md", max_chars: int = 60, time: bool = False) -> str:
    normalized = unicodedata.normalize("NFKD", prompt).encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")[:max_chars].rstrip("_")
    if not slug:
        import hashlib
        slug = f"generated_{hashlib.sha256(prompt.encode('utf-8')).hexdigest()[:12]}"
    if prefix:
        slug = f"{prefix}_{slug}"
    if suffix:
        slug = f"{slug}_{suffix}"
    if time:
        slug = f"{slug}_{strftime('%Y-%m-%d_%H-%M-%S', gmtime())}"
    return f"{slug}.{extension}" if extension else slug


def generate_output_file(prompt: str, extension: str = "md", max_chars: int = 60, time: bool = True) -> str:
    return generate_filename(prompt, extension=extension, max_chars=max_chars, time=time)


def chat(
    prompt: str = "",
    sys_msg: str = "You are a precise assistant.",
    msgs=None,
    funcs=None,
    model: str = "gpt-4o-mini",
    max_retry: int = 1,
    backoff_factor: float = 2,
    initial_wait: float = 0.25,
    *,
    client: Any = None,
) -> Union[str, dict]:
    messages = [{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}]
    messages.extend(msgs or [])
    provider = _openai_client(client)
    attempts = 0
    while True:
        try:
            kwargs = {"model": model, "messages": messages}
            if funcs:
                kwargs.update({"functions": funcs, "function_call": "auto"})
            response = provider.chat.completions.create(**kwargs)
            function_call = _function_call(response)
            if function_call:
                if hasattr(function_call, "model_dump"):
                    function_call = function_call.model_dump()
                elif not isinstance(function_call, dict):
                    function_call = dict(function_call)
                arguments = function_call.get("arguments")
                if isinstance(arguments, str):
                    function_call["arguments"] = json.loads(arguments)
                return function_call
            return _message_content(response)
        except LLMProviderError:
            raise
        except Exception as error:
            attempts += 1
            if attempts > max_retry:
                raise LLMProviderError("PROVIDER_REQUEST_FAILED", str(error)) from error
            sleep(initial_wait * (backoff_factor ** (attempts - 1)))


async def achat(
    prompt: str = "",
    sys_msg: str = "You are a precise assistant.",
    msgs=None,
    funcs=None,
    model: str = "gpt-4o-mini",
    max_retry: int = 1,
    backoff_factor: float = 2,
    initial_wait: float = 0.25,
    *,
    client: Any = None,
) -> Union[str, dict]:
    messages = [{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}]
    messages.extend(msgs or [])
    provider = _async_openai_client(client)
    attempts = 0
    while True:
        try:
            kwargs = {"model": model, "messages": messages}
            if funcs:
                kwargs.update({"functions": funcs, "function_call": "auto"})
            response = await provider.chat.completions.create(**kwargs)
            function_call = _function_call(response)
            if function_call:
                if hasattr(function_call, "model_dump"):
                    function_call = function_call.model_dump()
                arguments = function_call.get("arguments")
                if isinstance(arguments, str):
                    function_call["arguments"] = json.loads(arguments)
                return function_call
            return _message_content(response)
        except LLMProviderError:
            raise
        except Exception as error:
            attempts += 1
            if attempts > max_retry:
                raise LLMProviderError("PROVIDER_REQUEST_FAILED", str(error)) from error
            await asyncio.sleep(initial_wait * (backoff_factor ** (attempts - 1)))
