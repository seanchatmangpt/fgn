fgn --help
Usage: fgn [OPTIONS] COMMAND [ARGS]...

Options:
-m, --model TEXT The OpenAI model to be used for AGI response.
-i, --input TEXT Path to input file.
-o, --output TEXT Path to output file.
-pr, --prompt TEXT Prompt itself as a string.
-v, --verbose Enable verbose mode for printing output.
-t, --template TEXT Path to template file.
-e, --example TEXT Path to example file.
--clear-history Clear the history file.
-ao, --auto-output Automatically output to file with automatic
file name.
-as, --auto-summarize INTEGER Automatic summarization after the specified
number of messages.
-p, --paste Paste input from the clipboard.
-nc, --no-copy Do not copy output to the clipboard.
-tk, --tokens TEXT Token replacement separated by ;
-ext, --extension TEXT File extension of auto output file.
-d, --dsl TEXT Use the FGN Domain Specific Language.
--help Show this message and exit.

Commands:
blog Create a blog article.
chapter Create chapter.
code Create a code snippet.
guide Execute the guide command.
help Get help with the FGN CLI.
howto Create a how-to article.
nano Create a Nano Fiction story.
plan Create a plan like a Submarine Captain.
prompt Create a new prompt
shell Create a shell script.
summary Execute the summary command.
va Human Virtual Assistant usage tutor.

import os
import importlib.util
import click

from fgn.core import dsl_parser
from fgn.core.command_context import CommandContext
from fgn.core.core_cmd import core_command

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
ctx.obj = create_command_context(ctx.params)

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
@click.option('-m', '--model', default='gpt-3.5-turbo', help='The OpenAI model to be used for AGI response.')
@click.option('-i', '--input', help='Path to input file.')
@click.option('-o', '--output', help='Path to output file.')
@click.option('-pr', '--prompt', help='Prompt itself as a string.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose mode for printing output.')
@click.option('-t', '--template', help='Path to template file.')
@click.option('-e', '--example', help='Path to example file.')
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
@click.pass_context
def fgn(ctx, model, input, output, prompt, verbose, no_copy, paste, example, template, clear_history, auto_output,
auto_summarize, tokens, extension, dsl, text=""):

# Validate input before creating CommandContext

# try:

# validate_input(text, input, paste)

# except ValueError as ve:

# print(str(ve))

# return

    fgn_ctx = create_command_context(ctx.params)

    if dsl:
        dsl_parser.main(dsl, fgn_ctx)

    if verbose:
        print(fgn_ctx)

# Validate that at least one of text, input, or paste is provided

def validate_input(input, paste):
if not input and not paste:
raise ValueError("Please provide at least one of the following: a text, an input file, or paste input.")

def create_command_context(params):

# handle null params

if not params:
return CommandContext()
model = params['model']
input = params['input']
output = params['output']
prompt = params['prompt']
verbose = params['verbose']
no_copy = params['no_copy']
paste = params['paste']
example = params['example']
template = params['template']
clear_history = params['clear_history']
auto_output = params['auto_output']
text = ''
auto_summarize = params['auto_summarize']
tokens = params['tokens']
extension = params['extension']

    return CommandContext(model=model, input=input, output=output, prompt=prompt, verbose=verbose, no_copy=no_copy,
                          paste=paste, example=example, template=template, clear_history=clear_history,
                          auto_output=auto_output, text=text, auto_summarize=auto_summarize,
                          tokens=tokens, extension=extension)

if __name__ == "__main__":
fgn()

def gpt_chat_completion(messages, model, max_retry=5,
backoff_factor=2, initial_wait=1):
"""
Sends chat inputs to OpenAI API and receives the chatbot response.

    Args:
        messages (List[Dict]): A list of messages with role and content.
        model (str, optional): The GPT model to be used.
        max_retry (int, optional): The maximum number of retries.
        backoff_factor (int, optional): The factor to exponentially increase the waiting time.
        initial_wait (float, optional): The initial waiting time between retries in seconds.

    Returns:
        str: The content of the message generated by the chatbot.
    """

    # Initialize retry attempts
    retry = 0

    # Run the loop for retry attempts
    while retry <= max_retry:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            text = response['choices'][0]['message']['content'].strip()
            save_completion(text)
            return text
        except Exception as oops:
            # If the error is due to maximum context length, return the error message so that the user can handle it
            if "maximum context length" in str(oops):
                return f"GPT error: {oops}"

            retry += 1  # Increment the retry attempts

            # If reached the maximum retry attempts, return the error message
            if retry > max_retry:
                return f"GPT error: {oops}"

            # Calculate the waiting time for exponential backoff
            wait_time = initial_wait * (backoff_factor ** (retry - 1))

            # Print the error and wait before retrying
            print(f"Error communicating with OpenAI (attempt {retry}/{max_retry}): {oops}")
            sleep(wait_time)

You are a specialized AI chatbot designed to assist users with the FGN command line tool. As an FGN CLI help AGI, your
goal is to educate users on how to use the tool effectively and efficiently.

To answer the question of how to best answer a question using the FGN command line tool, let's break down the steps into
a step-by-step process that can be easily followed.

Step 1: Open the Command Prompt
To use FGN, the first step is to open the Command Prompt by searching for "cmd" in the Start menu or by pressing the
Windows key + R and typing "cmd" in the Run dialog box.

Step 2: Navigate to the directory where FGN is installed
Once the Command Prompt is open, navigate to the directory where FGN is installed using the `cd` command. For example,
if FGN is installed in the "C:\fgn" directory, type `cd C:\fgn` and press Enter.

Step 3: Choose the FGN command
To use FGN, type `fgn`, followed by the command, and any necessary arguments. For example, to create a business plan,
you would type `fgn -o business_plan.txt plan "My Business Plan"`.

Step 4: Specify input and output files
Before executing your command, make sure to specify the correct input and output files using the `-i` and `-o` options.
You can also use the `paste` option to paste text directly from the clipboard.

Step 5: View a list of available options and commands
To view a list of available options and commands, use the `help` command. For example, you can type `fgn help` to view
the FGN help page.

Step 6: Experiment and try different commands and options
Don't be afraid to experiment with different commands and options. The more you use FGN, the more comfortable you will
become with its capabilities and limitations.

By following these steps, you can effectively use the FGN command line tool to create smart to-do lists, generate unit
tests, execute shell scripts, and optimize your everyday tasks in a hassle-free manner.

In conclusion, the FGN command line tool is a powerful utility that can simplify file generation efficiently. With
practice and familiarity, it can become a robust tool for creating and manipulating files and data. As an FGN CLI Help
AGI, my goal is to educate users on the efficient use of this tool. Feel free to experiment with the FGN command line
tool and explore its limitless potential!