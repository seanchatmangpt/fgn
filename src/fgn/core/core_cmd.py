# fgn/core/core_cmd.py
from rich import print
from rich.markdown import Markdown

from fgn.core.chat_agent import ChatAgent
from fgn.utils.clipboard import paste_into_fgn, copy_into_clipboard
from fgn.utils.file_operations import open_file_or_raise
from fgn.utils.openai_operations import generate_output_file

from time import sleep

from rich.columns import Columns
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.spinner import Spinner, SPINNERS


def core_command(ctx):
    print("Running core command...")

    # Use ChatAgent for handling input
    chat_agent = ChatAgent(
        system_prompt="You are a Hive-Mind Multi Agent AGI that is designed to answer questions and solve problems. "
                      "You utilize emergent behavior of LLMs to come up with better answers than any single LLM. "
                      "When a question has multiple answers, you will provide the best answer. You primary way to solve"
                      " problems is to help humans generate code to create systems that last.",
        model=ctx.model,
        auto_clear=ctx.clear_history,
        verbose=ctx.verbose
    )
    chat_prompt = ""
    if ctx.prompt:
        chat_prompt += ctx.prompt + " "

    if ctx.schema:
        chat_prompt += open_file_or_raise(ctx.schema) + "\n"
    if ctx.template:
        chat_prompt += open_file_or_raise(ctx.template) + "\n"
    if ctx.example:
        chat_prompt += open_file_or_raise(ctx.example) + "\n"
    if ctx.input:
        chat_prompt += open_file_or_raise(ctx.input) + "\n"
    if ctx.paste:
        chat_prompt += paste_into_fgn() + " "
    # Add text to the chat_prompt
    if ctx.text:
        chat_prompt += ctx.text + " "
    if ctx.verbose:
        print(f"Input: {chat_prompt}")

    if not chat_prompt.strip():
        raise ValueError("Error: chat_prompt is empty. Please provide a prompt, input, text, or paste.")

    try:
        response = chat_agent.submit(chat_prompt, ctx.tokens)
    except Exception as e:
        print(f"Error: {e}")
        raise e

    if ctx.output or ctx.auto_output:
        if not ctx.output:
            ctx.output = generate_output_file(response)
        if ctx.append:
            with open(ctx.output, 'a') as output_file:
                output_file.write('\n\n' + response)
        else:
            with open(ctx.output, 'w') as output_file:
                output_file.write(response)
        if ctx.verbose:
            print(f"The output has been saved to {ctx.output}.")
    if not ctx.no_copy:
        copy_into_clipboard(response)

    md = Markdown(str(response))
    print(md)
