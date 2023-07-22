# fgn/core/commands/howto/howto_cmd.py
from pathlib import Path
import click

from fgn.core.default_sub_cmd import default_sub_cmd

cmd_name = Path(__file__).stem.split('_')[0]


@click.command()
@click.argument('text', required=False, default='')
@click.pass_context
def cli(ctx: click.Context, text) -> None:
    """Create a how-to article."""
    ctx.obj.text = text
    # ctx.obj.auto_output = True
    default_sub_cmd(ctx, cmd_name, prompt_prefix="Write a How to Article 'How to ",
                    prompt_suffix="' in the format of a how-to article.\n\n# How to Article\n\n")
