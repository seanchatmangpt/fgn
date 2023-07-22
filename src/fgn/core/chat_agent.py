import json
import os
from dataclasses import dataclass
from typing import List

from fgn.models.message import Message
from fgn.utils.file_operations import save_to_project_folder
from fgn.utils.openai_operations import gpt_chat_completion


@dataclass
class ChatAgent:
    model: str
    system_prompt: str = None
    messages: List[Message] = None
    auto_summarize: int = 4
    auto_clear: bool = False
    verbose: bool = False
    tokens: str = None
    history_path: str = None

    def __post_init__(self):
        if not self.messages:
            self.messages = []
        if self.system_prompt:
            self.messages.append(Message('system', self.system_prompt))
        if self.auto_clear:
            self.clear()
        else:
            if self.history_path:
                self.load()

    def submit(self, content, tokens=None):
        if self.verbose:
            print("ChatAgent.submit: ", content)

        # If tokens are provided, replace any {key} with the corresponding value
        # separated by a semicolon
        if self.tokens:
            for token in self.tokens.split(';'):
                key, value = token.split('=')
                content = content.replace("{{" + key + "}}", value)

        self.add_message('user', content)

        response = self.generate_response()

        # Check if the response contains the "maximum context length" error
        if "maximum context length" in response:
            # Auto-summarize the conversation
            success = self.summarize_conversations(self.auto_summarize)

            # If the summary was successful, generate a new response
            if success:
                response = self.generate_response()

        return response

    def add_message(self, role, content):
        self.messages.append(Message(role, content))

    def save(self):
        input_data = {
            "messages": [message.serialize() for message in self.messages]
        }

    def load(self):
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r', encoding='utf-8') as infile:
                    input_data = json.load(infile)
                    self.messages = [Message.deserialize(message_data) for message_data in input_data["messages"]]
            except json.JSONDecodeError:
                self.clear()

    def clear(self):
        # clear the messages except the first which is the system prompt
        self.messages = self.messages[:1]
        self.save()

    def generate_response(self):
        messages = [m.serialize() for m in self.messages]

        response = gpt_chat_completion(messages, model=self.model)

        if "maximum context length" in response:
            return response

        message = Message('assistant', response)
        self.add_message(message.role, message.content)
        if self.history_path:
            self.save()

        if self.verbose:
            print(message.content)

        return message.content

    def get_user_messages(self):
        return [msg for msg in self.messages if msg.role == 'user']

    def summarize_conversations(self, num_conversations: int, summary_length: int = 200) -> bool:
        if self.verbose:
            print("ChatAgent.summarize_conversations: ", num_conversations, summary_length)

        if num_conversations <= 0:
            return False

        while num_conversations > 0:
            # Collect the first 'num_conversations' user-assistant message pairs but skip the system prompt
            conversations = self.messages[1:(num_conversations * 2)]

            # Concatenate the user-assistant message pairs
            conversation_text = '\n'.join([f"{msg.role}: {msg.content}" for msg in conversations])

            # Set the summarizer AGI prompt
            summarizer_prompt = "You are a Summarizer AGI, an autonomous and intelligent text summarizer."

            # Generate a summary request
            summary_request = f"Please give a perfect executive summary of the salient points of the conversation in " \
                              f"about {summary_length} about words.:\n{conversation_text}"

            # Create a message list for the summary prompt
            summary_prompt_messages = [
                {'role': 'system', 'content': summarizer_prompt},
                {'role': 'user', 'content': summary_request}
            ]

            # Submit the summary prompt to gpt_chat_completion and get the response
            summary = gpt_chat_completion(summary_prompt_messages, model=self.model)

            if self.verbose:
                print("ChatAgent.summarize_conversations: ", summary)
                print("ChatAgent.summarize: " + summary)

            # If the response contains the "maximum context length" error,
            # reduce the number of conversations and try again
            if "maximum context length" in summary:
                num_conversations -= 1
                continue

            # Check if a summary was generated
            if not summary:
                return False

            # Remove the first 'num_conversations' user-assistant message pairs from the message list
            self.messages = [self.messages[0]] + self.messages[(num_conversations * 2) + 1:]

            # Update the messages with the summary request and response
            self.messages.insert(1, Message('user', f"Please summarize the first {num_conversations} conversations."))
            self.messages.insert(2, Message('assistant', summary))

            # Save the updated chat history
            self.save()

            return True

        return False

    def __str__(self):
        return '\n'.join([f"{m.role}: {m.content}" for m in self.messages])

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, index):
        return self.messages[index]
