import asyncio
import json
import os
from time import sleep
from typing import Union

import openai
from logger import logger


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
                    model=model, messages=messages, functions=funcs, function_call="auto"
                )
            else:
                response = openai.ChatCompletion.create(
                    model=model, messages=messages
                )
            function_call = (
                response.get("choices", [{}])[0].get("message", {}).get("function_call")
            )
            if function_call:
                print('WTF???', function_call)
                function_call["arguments"] = json.loads(function_call.get("arguments", ""))
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
                    model=model, messages=messages, functions=funcs, function_call="auto"
                )
            else:
                response = await openai.ChatCompletion.acreate(
                    model=model, messages=messages
                )
            function_call = (
                response.get("choices", [{}])[0].get("message", {}).get("function_call")
            )
            if function_call:
                print('WTF???', function_call)
                function_call["arguments"] = json.loads(function_call.get("arguments", ""))
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
            await asyncio.sleep(wait_time)

from dataclasses import dataclass, field
from typing import List, Union
import copy


@dataclass
class History:
    messages: List[dict] = field(default_factory=list)

    def append_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def last_message(self):
        return self.messages[-1] if self.messages else None

    @staticmethod
    def from_existing_history(existing_history):
        return History(copy.deepcopy(existing_history.messages))


def hchat(
    history: History,
    prompt: str = "",
    sys_msg: str = "A LLM 7 AGI Hive-Mind simulator",
    model: str = "gpt-3.5-turbo-0613",
    funcs: List[dict] = None,
    max_retry: int = 1,
    backoff_factor: int = 2,
    initial_wait: float = 0.25,
) -> History:
    """
    Pure function that takes a History object, interacts with the OpenAI API, and returns a new History object containing
    all previous messages and the new ones.
    """
    new_history = History.from_existing_history(history)
    new_history.append_message("user", prompt)

    response = chat(
        prompt=prompt,
        sys_msg=sys_msg,
        msgs=new_history.messages,
        funcs=funcs,
        model=model,
        max_retry=max_retry,
        backoff_factor=backoff_factor,
        initial_wait=initial_wait,
    )

    if isinstance(response, dict) and "name" in response:
        available_functions = {func["name"]: func for func in funcs}
        function_name = response["name"]
        function_to_call = available_functions.get(function_name)
        if function_to_call:
            function_args = response["arguments"]
            function_response = function_to_call(**function_args)
            new_history.append_message("function", json.dumps(function_response))
            return new_history

    new_history.append_message("assistant", response)

    return new_history

from typing import Callable
import random

class RapBattleAgent:
    def __init__(self, name: str, human_input_mode: str = "NEVER", system_message: str = ""):
        self.name = name
        self.human_input_mode = human_input_mode
        self.system_message = system_message

    def reply(self, prompt: str, history: History) -> History:
        response = hchat(
            history=history,
            prompt=prompt,
            sys_msg=self.system_message,
        )
        print(f"{self.name}: {response.last_message()['content']}")
        return response


class GroupChatManager:
    def __init__(self, agents: List[RapBattleAgent], group_chat: List[dict] = None):
        self.agents = agents
        self.group_chat = group_chat if group_chat else []

    def conduct_rap_battle(self, rounds: int = 3) -> List[dict]:
        judge = next((agent for agent in self.agents if agent.name == "Eminem"), None)
        contestants = [agent for agent in self.agents if agent != judge]
        if not judge or len(contestants) != 2:
            raise ValueError("Invalid setup for rap battle.")

        for round_num in range(rounds):
            for contestant in contestants:
                prompt = f"Round {round_num + 1}: {contestant.name}, it's your turn to rap!"
                print(prompt)
                history = History(self.group_chat)
                new_history = contestant.reply(prompt, history)
                self.group_chat = new_history.messages

            prompt_judge = f"Round {round_num + 1} is over. Eminem, who won this round?"
            print(prompt_judge)
            history_judge = History(self.group_chat)
            new_history_judge = judge.reply(prompt_judge, history_judge)
            print(f"Eminem: {new_history_judge.last_message()['content']}")
            self.group_chat = new_history_judge.messages

        return self.group_chat


# Setup
kool_keith = RapBattleAgent(name="Kool Keith", system_message="You are Kool Keith, rap battle!")
xzibit = RapBattleAgent(name="Xzibit", system_message="You are Xzibit, rap battle!")
eminem = RapBattleAgent(name="Eminem", system_message="You are Eminem, the judge of this rap battle!")

group_chat_manager = GroupChatManager(agents=[kool_keith, xzibit, eminem])

# Conducting the rap battle
rap_battle_history = group_chat_manager.conduct_rap_battle()
print(rap_battle_history)
