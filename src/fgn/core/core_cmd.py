from rich import print

from fgn.core.chat_agent import ChatAgent
from fgn.utils.clipboard import paste_into_fgn
from fgn.utils.file_operations import open_file_or_raise
from fgn.utils.output_manager import OutputManager


def core_command(ctx):
    chat_agent = ChatAgent(
        system_prompt=(
            "You are a multi-agent assistant designed to answer questions and help humans "
            "manufacture durable systems."
        ),
        model=ctx.model,
        auto_clear=ctx.clear_history,
        verbose=ctx.verbose,
        tokens=ctx.tokens,
    )
    prompt_parts = []
    if ctx.prompt:
        prompt_parts.append(ctx.prompt)
    for path in (ctx.schema, ctx.template, ctx.example, ctx.input):
        if path:
            prompt_parts.append(open_file_or_raise(path))
    if ctx.paste:
        prompt_parts.append(paste_into_fgn())
    if ctx.text:
        prompt_parts.append(ctx.text)
    chat_prompt = "\n".join(prompt_parts).strip()
    if not chat_prompt:
        raise ValueError("Please provide a prompt, input, text, or clipboard content.")
    if ctx.verbose:
        print(f"Input: {chat_prompt}")
    response = chat_agent.submit(chat_prompt, ctx.tokens)
    manager = OutputManager(
        output=ctx.output,
        no_copy=ctx.no_copy,
        auto_output=ctx.auto_output,
        verbose=ctx.verbose,
        extension=ctx.extension or "md",
    )
    return manager.handle_output(response, append=bool(ctx.append))
