# fgn/core/commands/shell/shell_cmd.py
from pathlib import Path
import click
import platform
from os import getenv
from os.path import basename, splitext
from distro import name as distro_name

from fgn.core.default_sub_cmd import default_sub_cmd

cmd_name = Path(__file__).stem.split('_')[0]


@click.command()
@click.argument('text', required=False, default='')
@click.pass_context
def cli(ctx: click.Context, text) -> None:
    """Create a shell script."""
    operating_systems = {
        "Linux": "Linux/" + distro_name(pretty=True),
        "Windows": "Windows " + platform.release(),
        "Darwin": "Darwin/MacOS " + platform.mac_ver()[0],
    }
    current_platform = platform.system()
    os_name = operating_systems.get(current_platform, current_platform)
    shell_name = basename(getenv("SHELL", "PowerShell"))
    if os_name == "nt":
        shell_name = splitext(basename(getenv("COMSPEC", "Powershell")))[0]
    ctx.obj.text = text

    prompt_suffix = f"""###
Provide only {shell_name} commands for {os_name} without any description.
If there is a lack of details, provide most logical solution.
Ensure the output is a valid shell command.
If multiple steps required try to combine them together.
Prompt: {text}
###
Command:\n$"""

    ctx.obj.model = "gpt-3.5-turbo"
    default_sub_cmd(ctx, cmd_name, extract_md=True, prompt_suffix=prompt_suffix)
