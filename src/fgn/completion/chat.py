from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union

from fgn.completion.prompt_schemas import msg_schema, str_func_schema
from fgn.core.broker import Broker, Receipt
from fgn.utils.llm_operations import (
    achat as provider_achat,
    chat as provider_chat,
    generate_filename,
)

DEFAULT_PROMPT = ""
DEFAULT_SYS_MSG = "AI chatbot that converses like a LLM 7 AGI Hive-Mind simulator"
DEFAULT_MODEL = "4"
DEFAULT_MAX_RETRY = 5
DEFAULT_BACKOFF_FACTOR = 2
DEFAULT_INITIAL_WAIT = 0.25


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
    mode="a+",
    *,
    client: Any = None,
) -> Union[str, dict]:
    """Compatibility facade over the admitted modern provider boundary."""
    result = provider_chat(
        prompt=prompt,
        sys_msg=sys_msg,
        msgs=msgs,
        funcs=funcs,
        model=get_model_str(model),
        max_retry=max_retry,
        backoff_factor=backoff_factor,
        initial_wait=initial_wait,
        client=client,
    )
    write_response(mode, prompt, result, write_path)
    if raw_msg and isinstance(result, str):
        return {"role": "assistant", "content": result}
    return result


@dataclass
class Chat:
    prompt: str = DEFAULT_PROMPT
    sys_msg: str = DEFAULT_SYS_MSG
    msgs: list[dict[str, Any]] | None = None
    funcs: list[dict[str, Any]] | None = None
    model: str = DEFAULT_MODEL
    max_retry: int = DEFAULT_MAX_RETRY
    backoff_factor: float = DEFAULT_BACKOFF_FACTOR
    initial_wait: float = DEFAULT_INITIAL_WAIT
    raw_msg: bool = False
    write_path: str | None = None
    mode: str = "a+"
    client: Any = None

    def __call__(self, **kwargs):
        values = {
            "prompt": self.prompt,
            "sys_msg": self.sys_msg,
            "msgs": self.msgs,
            "funcs": self.funcs,
            "model": self.model,
            "max_retry": self.max_retry,
            "backoff_factor": self.backoff_factor,
            "initial_wait": self.initial_wait,
            "raw_msg": self.raw_msg,
            "write_path": self.write_path,
            "mode": self.mode,
            "client": self.client,
        }
        values.update(kwargs)
        return chat(**values)


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
    write_path=None,
    mode="a+",
    *,
    client: Any = None,
) -> Union[str, dict]:
    result = await provider_achat(
        prompt=prompt,
        sys_msg=sys_msg,
        msgs=msgs,
        funcs=funcs,
        model=get_model_str(model),
        max_retry=max_retry,
        backoff_factor=backoff_factor,
        initial_wait=initial_wait,
        client=client,
    )
    await awrite_response(mode, prompt, result, write_path)
    if raw_msg and isinstance(result, str):
        return {"role": "assistant", "content": result}
    return result


def _resolved_write_path(prompt: str, write_path: str) -> Path:
    path = Path(write_path)
    if path.is_dir():
        path = path / generate_filename(prompt)
    return path


def write_response(mode, prompt, res, write_path) -> Receipt | None:
    if not write_path:
        return None
    append = "a" in mode
    content = f"{res}\n"
    return Broker().write_text(
        _resolved_write_path(prompt, write_path),
        content,
        append=append,
    )


async def awrite_response(mode, prompt, res, write_path) -> Receipt | None:
    return write_response(mode, prompt, res, write_path)


def get_response(res, raw_msg, funcs):
    """Decode legacy mapping-shaped provider responses for compatibility."""
    if hasattr(res, "model_dump"):
        res = res.model_dump()
    msg = res.get("choices", [{}])[0].get("message", {})
    if raw_msg:
        return msg
    func = msg.get("function_call")
    if func:
        arguments = func.get("arguments", "")
        if isinstance(arguments, str):
            try:
                func["arguments"] = json.loads(arguments)
            except json.JSONDecodeError:
                pass
        if not isinstance(func.get("arguments"), dict):
            raise ValueError(f"Invalid function response from provider: {msg}")
        return func
    if funcs:
        raise ValueError(f"Invalid function response from provider: {msg}")
    return str(msg.get("content", "")).strip()


def get_model_str(model):
    aliases = {
        "3": os.getenv("FGN_FAST_MODEL", "gpt-4o-mini"),
        "3i": os.getenv("FGN_FAST_MODEL", "gpt-4o-mini"),
        "4": os.getenv("FGN_MODEL", "gpt-4o"),
    }
    return aliases.get(str(model), model)


def _create_params(model, messages, funcs=None):
    parameters = {"model": get_model_str(model), "messages": messages}
    if funcs:
        parameters["functions"] = funcs
        parameters["function_call"] = "auto"
    return parameters


def _create_messages(sys_msg, prompt, msgs):
    messages = [{"role": "system", "content": sys_msg}]
    if prompt:
        messages.append({"role": "user", "content": prompt})
    messages.extend(msgs or [])
    return messages


def shell_command():
    messages = [
        msg_schema("What is the shell command to create a python project with pyscaffold?")
    ]
    functions = [
        str_func_schema(
            "execute_shell",
            "A shell command to execute in one line. No explanation or description needed.",
            "command",
            "The shell command to execute in one line. No explanation or description neded.",
        )
    ]
    response = chat(
        sys_msg=(
            "Return only a shell command that creates the requested project. "
            "Do not execute it."
        ),
        msgs=messages,
        funcs=functions,
        model="3",
    )
    print(response)
