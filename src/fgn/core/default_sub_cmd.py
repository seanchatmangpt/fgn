import click
from rich import print

from fgn.utils.chat_agent_configuration import ChatAgentConfiguration
from fgn.utils.output_manager import OutputManager


def build_chat_agent_and_prompt(config):
    chat_prompt = config.build_chat_prompt()
    chat_agent = config.get_chat_agent()
    return chat_agent, chat_prompt


def handle_response(config, response, extract_md, append, extension):
    output_manager = OutputManager(output=config.get("output"),
                                   no_copy=config.get("no_copy"),
                                   auto_output=config.get("auto_output"),
                                   verbose=config.get("verbose"),
                                   extension=extension)
    output_manager.handle_output(response, extract_md=extract_md, append=append)


def default_sub_cmd(ctx, cmd_name: str, extract_md=False, prompt_prefix="", prompt_suffix=""):
    """Execute the default sub command."""

    fgn_context = ctx.obj
    config = ChatAgentConfiguration(fgn_context, cmd_name)
    chat_agent, chat_prompt = build_chat_agent_and_prompt(config)

    if config.get("verbose"):
        print(f"Running {cmd_name} command...")

    if prompt_prefix:
        chat_prompt = f"{prompt_prefix} {chat_prompt}"

    if prompt_suffix:
        chat_prompt = f"{chat_prompt} {prompt_suffix}"

    if config.get("verbose"):
        print(f"Input: {chat_prompt}")

    response = chat_agent.submit(chat_prompt)

    handle_response(config, response, extract_md, fgn_context.append, fgn_context.extension)

    if config.get("verbose"):
        print(f"Output: {response}")
