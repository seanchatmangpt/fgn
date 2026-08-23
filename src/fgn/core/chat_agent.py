import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from fgn.core.broker import Broker
from fgn.models.message import Message
from fgn.utils.llm_operations import LLMProviderError, gpt_chat_completion


@dataclass
class ChatAgent:
    model: str
    system_prompt: Optional[str] = None
    messages: Optional[List[Message]] = None
    auto_summarize: int = 4
    auto_clear: bool = False
    verbose: bool = False
    tokens: Optional[str] = None
    history_path: Optional[str] = None

    def __post_init__(self):
        if self.messages is None:
            self.messages = []
        if self.system_prompt and not self.messages:
            self.messages.append(Message("system", self.system_prompt))
        if self.auto_clear:
            self.clear()
        elif self.history_path:
            self.load()

    def submit(self, content, tokens=None):
        replacements = tokens or self.tokens
        if replacements:
            for token in replacements.split(";"):
                if "=" not in token:
                    raise ValueError(f"Invalid token replacement: {token!r}")
                key, value = token.split("=", 1)
                content = content.replace("{{" + key + "}}", value)
        self.add_message("user", content)
        try:
            return self.generate_response()
        except LLMProviderError as error:
            if error.code != "CONTEXT_LENGTH_EXCEEDED":
                raise
            if self.summarize_conversations(self.auto_summarize):
                return self.generate_response()
            raise

    def add_message(self, role, content):
        self.messages.append(Message(role, content))

    def save(self):
        if not self.history_path:
            return None
        payload = json.dumps({"messages": [message.serialize() for message in self.messages]}, indent=2) + "\n"
        return Broker().write_text(Path(self.history_path).expanduser(), payload)

    def load(self):
        path = Path(self.history_path).expanduser()
        if not path.exists():
            return
        try:
            input_data = json.loads(path.read_text(encoding="utf-8"))
            self.messages = [Message.deserialize(item) for item in input_data["messages"]]
        except (json.JSONDecodeError, KeyError, TypeError):
            self.clear()

    def clear(self):
        self.messages = self.messages[:1] if self.messages and self.messages[0].role == "system" else []
        return self.save()

    def generate_response(self):
        response = gpt_chat_completion([m.serialize() for m in self.messages], model=self.model)
        self.add_message("assistant", response)
        if self.history_path:
            self.save()
        return response

    def get_user_messages(self):
        return [msg for msg in self.messages if msg.role == "user"]

    def summarize_conversations(self, num_conversations: int, summary_length: int = 200) -> bool:
        if num_conversations <= 0 or len(self.messages) < 3:
            return False
        conversations = self.messages[1 : (num_conversations * 2) + 1]
        conversation_text = "\n".join(f"{msg.role}: {msg.content}" for msg in conversations)
        summary = gpt_chat_completion(
            [
                {"role": "system", "content": "Summarize the conversation faithfully."},
                {"role": "user", "content": f"Summarize in about {summary_length} words:\n{conversation_text}"},
            ],
            model=self.model,
        )
        if not summary:
            return False
        system = self.messages[:1] if self.messages and self.messages[0].role == "system" else []
        remainder = self.messages[(num_conversations * 2) + 1 :]
        self.messages = system + [Message("assistant", summary)] + remainder
        self.save()
        return True

    def __str__(self):
        return "\n".join(f"{m.role}: {m.content}" for m in self.messages)

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, index):
        return self.messages[index]
