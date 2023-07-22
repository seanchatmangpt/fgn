# fgn/utils/chat_agent_configuration.py
from dataclasses import dataclass
from typing import Any, Dict, Optional
from fgn.core.chat_agent import ChatAgent
import os
import yaml

from fgn.core.command_context import CommandContext
from fgn.utils.clipboard import paste_into_fgn
from fgn.utils.file_operations import open_file_or_raise, get_project_root, open_file


@dataclass
class ChatAgentConfiguration:
    context: CommandContext
    cmd_name: str
    defaults: Dict[str, Any] = None

    def __post_init__(self):
        if self.defaults is None:
            self.defaults = self.load_default_yaml()

    def load_file_content(self, file_name: str) -> Optional[str]:
        file_path = os.path.join(get_project_root(), 'core', 'commands', self.cmd_name,
                                 file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

        return None

    def get(self, key: str, default: Any = None) -> Any:
        ctx_value = getattr(self.context, key, None)
        default_value = self.defaults.get(key, default)
        return ctx_value if ctx_value is not None else default_value

    def build_chat_prompt(self) -> str:
        chat_prompt = ""
        prompt = self.get('prompt')
        # get file or throw

        paste = self.context.paste

        # Retrieve the file names from the YAML configuration or context
        example_file = self.context.example
        template_file = self.context.template
        schema_file = self.context.schema

        # Load the file content using the load_file_content() method
        example = open_file(example_file) if example_file else None
        template = open_file(template_file) if template_file else None
        schema = open_file(schema_file) if schema_file else None

        if schema:
            chat_prompt += schema + "\n"
        if template:
            chat_prompt += template + "\n"
        if example:
            chat_prompt += example + "\n"
        if self.context.input:
            chat_prompt += open_file_or_raise(self.context.input) + "\n"
        if paste:
            chat_prompt += paste_into_fgn() + "\n"
        if prompt:
            chat_prompt += prompt + " "
        if self.context.text:
            chat_prompt += self.context.text + " "

        return chat_prompt

    def load_default_yaml(self) -> Dict[str, Any]:
        # Define the new location for the YAML files
        yaml_file = os.path.join(get_project_root(), 'core', 'commands', self.cmd_name,
                                 f"{self.cmd_name}_config.yml")

        config = {}
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)
        return config.get('defaults')

    def get_chat_agent(self) -> ChatAgent:
        chat_agent = ChatAgent(
            history_path=self.get('history_path'),
            model=self.get('model'),
            system_prompt=self.load_file_content(self.get('system_prompt')),
            auto_clear=self.get('clear_history', False),
            verbose=self.get('verbose', False),
            auto_summarize=self.get('auto_summarize', 4),
            tokens=self.context.tokens
        )
        return chat_agent
