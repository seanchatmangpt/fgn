# fgn/core/commands/core/core_cmd.py
from pathlib import Path
import click

from fgn.core.core_cmd import core_command
from fgn.core.default_sub_cmd import default_sub_cmd

cmd_name = Path(__file__).stem.split('_')[0]


@click.command()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """CLI internal usage only. Do not call directly."""
    core_command(ctx.obj)
