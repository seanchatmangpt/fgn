import json
from dataclasses import dataclass, field
from typing import List, Union, Dict, Any
from copy import deepcopy

from fgn.utils.llm_operations import chat


class History:
    _messages: List[Dict[str, Any]]

    def __init__(self, messages: List[dict] = None):
        self._messages = deepcopy(messages) if messages else []

    def chat(self, *args, **kwargs):
        from chat import chat

        msg = chat(raw_msg=True, *args, **kwargs)
        self._messages.append(msg)

    def last(self, role: str = None) -> Union[dict, None]:
        """
        Returns the last message in the history, optionally filtered by role.
        """
        if role:
            for msg in reversed(self._messages):
                if msg["role"] == role:
                    return msg
        else:
            return self._messages[-1]

    def __call__(self, *args, **kwargs):
        return self.chat(*args, **kwargs)

    def __len__(self):
        return len(self._messages)

    def __getitem__(self, index):
        return self._messages[index]

    def __iter__(self):
        return iter(self._messages)

    def __next__(self):
        # noinspection PyTypeChecker
        return next(self._messages)


h = History()


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
            new_history.append("function", json.dumps(function_response))
            return new_history

    new_history.append("assistant", response)

    return new_history


class RapBattleAgent:
    def __init__(
        self, name: str, human_input_mode: str = "NEVER", system_message: str = ""
    ):
        self.name = name
        self.human_input_mode = human_input_mode
        self.system_message = system_message

    def reply(self, prompt: str, history: History) -> History:
        response = hchat(
            history=history,
            prompt=prompt,
            sys_msg=self.system_message,
        )
        print(f"{self.name}: {response.last()['content']}")
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
                prompt = (
                    f"Round {round_num + 1}: {contestant.name}, it's your turn to rap!"
                )
                print(prompt)
                history = History(self.group_chat)
                new_history = contestant.reply(prompt, history)
                self.group_chat = new_history

            prompt_judge = f"Round {round_num + 1} is over. Eminem, who won this round?"
            print(prompt_judge)
            history_judge = History(self.group_chat)
            new_history_judge = judge.reply(prompt_judge, history_judge)
            print(f"Eminem: {new_history_judge.last()['content']}")
            self.group_chat = new_history_judge.messages

        return self.group_chat


# Setup
kool_keith = RapBattleAgent(
    name="Kool Keith", system_message="You are Kool Keith, rap battle!"
)
xzibit = RapBattleAgent(name="Xzibit", system_message="You are Xzibit, rap battle!")
eminem = RapBattleAgent(
    name="Eminem", system_message="You are Eminem, the judge of this rap battle!"
)

group_chat_manager = GroupChatManager(agents=[kool_keith, xzibit, eminem])

# Conducting the rap battle
rap_battle_history = group_chat_manager.conduct_rap_battle()
print(rap_battle_history)
