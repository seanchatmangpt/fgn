from __future__ import annotations

from typing import Any

from fgn.utils.llm_operations import achat, gpt_chat_completion


def get_model_str(model):
    if model == "3i":
        return "gpt-4o-mini"
    return model


def create(
    prompt: str,
    model="3i",
    temperature=0,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    *,
    client: Any = None,
):
    del temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop
    return gpt_chat_completion(
        [{"role": "user", "content": prompt}],
        model=get_model_str(model),
        client=client,
    )


async def acreate(
    prompt: str,
    model="3i",
    temperature=0,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    *,
    client: Any = None,
):
    del temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop
    return await achat(
        prompt=prompt,
        model=get_model_str(model),
        client=client,
    )
