from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, List, Union

from fgn.utils.llm_operations import chat


class History:
    """In-memory chat history with explicit provider execution."""

    def __init__(self, messages: Iterable[dict] | None = None):
        self._messages: List[Dict[str, Any]] = deepcopy(list(messages or []))

    @classmethod
    def from_existing_history(cls, history: "History") -> "History":
        return cls(history.messages)

    @property
    def messages(self) -> List[Dict[str, Any]]:
        return deepcopy(self._messages)

    def append(self, role: str, content: Any) -> None:
        self._messages.append({"role": role, "content": content})

    def chat(self, *args, **kwargs):
        message = chat(raw_msg=True, msgs=self.messages, *args, **kwargs)
        if isinstance(message, dict):
            self._messages.append(message)
        else:
            self.append("assistant", message)
        return message

    def last(self, role: str | None = None) -> Union[dict, None]:
        if role:
            return next((msg for msg in reversed(self._messages) if msg.get("role") == role), None)
        return self._messages[-1] if self._messages else None

    def __call__(self, *args, **kwargs):
        return self.chat(*args, **kwargs)

    def __len__(self):
        return len(self._messages)

    def __getitem__(self, index):
        return self._messages[index]

    def __iter__(self):
        return iter(self._messages)


def hchat(
    history: History,
    prompt: str = "",
    sys_msg: str = "You are a precise assistant.",
    model: str = "gpt-4o-mini",
    funcs: List[dict] | None = None,
    max_retry: int = 1,
    backoff_factor: int = 2,
    initial_wait: float = 0.25,
    *,
    client: Any = None,
) -> History:
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
        client=client,
    )
    new_history.append("assistant", response)
    return new_history


class RapBattleAgent:
    def __init__(self, name: str, human_input_mode: str = "NEVER", system_message: str = ""):
        self.name = name
        self.human_input_mode = human_input_mode
        self.system_message = system_message

    def reply(self, prompt: str, history: History, *, client: Any = None) -> History:
        return hchat(history=history, prompt=prompt, sys_msg=self.system_message, client=client)


class GroupChatManager:
    def __init__(self, agents: List[RapBattleAgent], group_chat: List[dict] | None = None):
        self.agents = agents
        self.group_chat = group_chat or []

    def conduct_rap_battle(self, rounds: int = 3, *, client: Any = None) -> List[dict]:
        judge = next((agent for agent in self.agents if agent.name == "Eminem"), None)
        contestants = [agent for agent in self.agents if agent is not judge]
        if not judge or len(contestants) != 2:
            raise ValueError("Invalid setup for rap battle.")
        for round_num in range(rounds):
            for contestant in contestants:
                history = contestant.reply(
                    f"Round {round_num + 1}: {contestant.name}, respond.",
                    History(self.group_chat),
                    client=client,
                )
                self.group_chat = history.messages
            self.group_chat = judge.reply(
                f"Round {round_num + 1} is over. Select the winner.",
                History(self.group_chat),
                client=client,
            ).messages
        return deepcopy(self.group_chat)


def demo(*, client: Any = None) -> List[dict]:
    agents = [
        RapBattleAgent("Kool Keith", system_message="You are Kool Keith."),
        RapBattleAgent("Xzibit", system_message="You are Xzibit."),
        RapBattleAgent("Eminem", system_message="You are the judge."),
    ]
    return GroupChatManager(agents).conduct_rap_battle(client=client)


if __name__ == "__main__":
    print(demo())
