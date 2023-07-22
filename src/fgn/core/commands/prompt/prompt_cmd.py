# fgn/core/commands/prompt/prompt_cmd.py
from pathlib import Path
import click

from fgn.core.default_sub_cmd import default_sub_cmd

cmd_name = Path(__file__).stem.split('_')[0]


@click.command()
@click.argument('text', required=False, default='')
@click.pass_context
def cli(ctx: click.Context, text) -> None:
    """Create a new prompt"""
    ctx.obj.text = text
    default_sub_cmd(ctx, cmd_name, extract_md=True, prompt_suffix='\nStart with "You are a " in your response.\n')
