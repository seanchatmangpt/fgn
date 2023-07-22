import os
import importlib.util
import click
from click import Context
from rich import print

from fgn.core import dsl_parser
from fgn.core.command_context import create_context
from fgn.core.core_cmd import core_command
from fgn.utils.file_operations import create_project_dir

COMMANDS_DIRECTORY = os.path.join(os.path.dirname(__file__), "commands")


class FGNCommandsLoader(click.MultiCommand):
    def list_commands(self, ctx):
        return get_command_folders(COMMANDS_DIRECTORY)

    def get_command(self, ctx, name):
        return load_command(ctx, name, COMMANDS_DIRECTORY)


# Get command folders in the specified directory
def get_command_folders(directory):
    command_folders = [folder_name for folder_name in os.listdir(directory) if
                       os.path.isdir(os.path.join(directory, folder_name))]
    command_folders.sort()
    return command_folders


# Load the command with the given name from the commands_directory
def load_command(ctx, name, commands_directory):
    ctx.obj = create_context(ctx.params)

    command_script = os.path.join(commands_directory, name, f"{name}_cmd.py")

    if name == '__pycache__':
        return None

    if os.path.isfile(command_script):
        spec = importlib.util.spec_from_file_location(f"{name}_command", command_script)
        command_obj = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(command_obj)
        command = command_obj.cli
        command.obj = ctx.obj
        return command
    else:
        # Load the core command
        command_script = os.path.join(commands_directory, 'core', f"core_cmd.py")
        spec = importlib.util.spec_from_file_location(f"core_command", command_script)
        command_obj = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(command_obj)
        command = command_obj.cli
        ctx.obj.text = name
        command.obj = ctx.obj
        return command


@click.group(invoke_without_command=True, cls=FGNCommandsLoader)
@click.option('-m', '--model', default='gpt-4', help='The OpenAI model to be used for AGI response.')
@click.option('-i', '--input', help='Path to input file.')
@click.option('-o', '--output', help='Path to output file.')
@click.option('-io', '--in-n-out', help='Path to input and output file.')
@click.option('-pr', '--prompt', help='Prompt itself as a string.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose mode for printing output.')
@click.option('-t', '--template', help='Path to template file.')
@click.option('-e', '--example', help='Path to example file.')
@click.option('-sp', '--system-prompt', help='Path to system prompt file.')
@click.option('-sc', '--schema', help='Path to response schema definition file.')
@click.option('--clear-history', is_flag=True, help='Clear the history file.')
@click.option('-ao', '--auto-output', is_flag=True, help='Automatically output to file with automatic file name.')
@click.option('-as', '--auto-summarize', type=int,
              help='Automatic summarization after the specified number of messages.',
              default=4)
@click.option('-p', '--paste', is_flag=True, help='Paste input from the clipboard.')
@click.option('-nc', '--no-copy', is_flag=True, help='Do not copy output to the clipboard.')
@click.option('-tk', '--tokens', help='Token replacement separated by ;')
@click.option('-ext', '--extension', help='File extension of auto output file.')
@click.option('-d', '--dsl', help='Use the FGN Domain Specific Language.')
@click.option('-a', '--append', is_flag=True, help='Append to the output file.')
@click.pass_context
def fgn(ctx: Context, model, input, output, prompt, verbose, no_copy, paste, example, template, clear_history,
        auto_output,
        auto_summarize, tokens, extension, dsl, system_prompt, schema, append, in_n_out, text=""):
    fgn_ctx = create_context(ctx.params)

    create_project_dir()

    if dsl:
        dsl_parser.main(dsl, fgn_ctx)

    if verbose:
        print(fgn_ctx)


# Validate that at least one of text, input, or paste is provided
def validate_input(input, paste):
    if not input and not paste:
        raise ValueError("Please provide at least one of the following: a text, an input file, or paste input.")


if __name__ == "__main__":
    fgn()
