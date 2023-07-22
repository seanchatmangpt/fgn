import os
from pathlib import Path
import yaml
import re

from fgn.core.command_context import CommandContext


def load_default_or_context(fgn_context: CommandContext, yaml_file):
    config = {}
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)

    defaults = config.get('defaults')

    model = fgn_context.model if fgn_context.model else defaults.get('model', 'gpt-3.5-turbo')
    history_path = defaults.get('history_path', 'history.txt')
    auto_clear = fgn_context.clear_history if fgn_context.clear_history is not None else defaults.get('auto_clear',
                                                                                                      False)
    verbose = fgn_context.verbose if fgn_context.verbose is not None else defaults.get('verbose', False)
    auto_summarize = defaults.get('auto_summarize', 4)

    system_prompt = fgn_context.prompt if fgn_context.prompt else defaults.get('system_prompt', 'system_prompt.txt')

    example = fgn_context.example if fgn_context.example else defaults.get('example')
    template = fgn_context.template if fgn_context.template else defaults.get('template')
    input = fgn_context.input
    prompt = fgn_context.prompt

    return model, history_path, auto_clear, verbose, auto_summarize, system_prompt, example, template, input, prompt


def open_file(filepath):
    filepath = get_norm_path(filepath)
    abs_path = os.path.abspath(filepath)
    with open(abs_path, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_relative_to_base(filepath, content, base_path=None):
    filepath = get_norm_path(filepath)

    if base_path is None:
        base_path = os.path.dirname(os.path.abspath(__file__))

    abs_path = os.path.join(base_path, filepath)

    with open(abs_path, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def open_file_or_raise(path: str) -> str:
    path = get_norm_path(path)

    if os.path.isfile(path):
        abs_path = os.path.abspath(path)
        with open(abs_path, 'r') as file:
            return file.read()
    else:
        raise FileNotFoundError('File not found')


def extract_markdown(text: str) -> str:
    markdown = re.findall(r'```(.*?)```', text, re.DOTALL)

    if len(markdown) == 0:
        return text
    else:
        markdown = [m.replace(m.split('\n')[0], '') for m in markdown]
        markdown = [m.replace('\n', '', 1) for m in markdown]
        return '\n'.join(markdown)


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_norm_path(path: str) -> str:
    if os.name == "nt":
        return os.path.normpath(path).replace("/", "\\")
    else:
        return os.path.normpath(path)


def save_to_project_folder(file_path, content):
    file = Path.home() / '.fgn' / file_path
    print(f"Saving to {file}")

    # Write the required directories if they don't exist
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))

    with open(file, 'w', encoding='utf-8') as outfile:
        print(f"Writing to {file}")
        outfile.write(content)


def create_project_dir():
    fgn_dir = Path.home() / '.fgn'
    try:
        if not os.path.exists(fgn_dir):
            os.makedirs(fgn_dir)
    except OSError:
        print(f"Creation of the directory %s failed {fgn_dir}")
