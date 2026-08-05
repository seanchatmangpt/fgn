import os
import re
from pathlib import Path

import yaml

from fgn.core.broker import Broker, Receipt
from fgn.core.command_context import CommandContext


def load_default_or_context(fgn_context: CommandContext, yaml_file):
    with open(yaml_file, encoding="utf-8") as file:
        config = yaml.safe_load(file)
    defaults = config.get("defaults", {})
    model = fgn_context.model or defaults.get("model", "gpt-3.5-turbo")
    history_path = defaults.get("history_path", "history.txt")
    auto_clear = fgn_context.clear_history if fgn_context.clear_history is not None else defaults.get("auto_clear", False)
    verbose = fgn_context.verbose if fgn_context.verbose is not None else defaults.get("verbose", False)
    auto_summarize = defaults.get("auto_summarize", 4)
    system_prompt = fgn_context.prompt or defaults.get("system_prompt", "system_prompt.txt")
    example = fgn_context.example or defaults.get("example")
    template = fgn_context.template or defaults.get("template")
    return model, history_path, auto_clear, verbose, auto_summarize, system_prompt, example, template, fgn_context.input, fgn_context.prompt


def open_file(filepath):
    return Path(get_norm_path(filepath)).expanduser().read_text(encoding="utf-8")


def save_relative_to_base(filepath, content, base_path=None) -> Receipt:
    base = Path(base_path) if base_path else Path(__file__).resolve().parent
    return Broker().write_text(base / get_norm_path(filepath), content)


def open_file_or_raise(path: str) -> str:
    normalized = Path(get_norm_path(path)).expanduser()
    if not normalized.is_file():
        raise FileNotFoundError(f"File not found: {normalized}")
    return normalized.read_text(encoding="utf-8")


def extract_markdown(text: str) -> str:
    markdown = re.findall(r"```(.*?)```", text, re.DOTALL)
    if not markdown:
        return text
    blocks = [block.replace(block.split("\n")[0], "", 1).replace("\n", "", 1) for block in markdown]
    return "\n".join(blocks)


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_norm_path(path: str) -> str:
    return os.path.normpath(path)


def save_to_project_folder(file_path, content) -> Receipt:
    return Broker().write_text(Path.home() / ".fgn" / file_path, content)


def create_project_dir():
    return Broker().receipt_dir.parent
