# fgn/core/commands/chain/chain_cmd.py
from pathlib import Path
import click

from fgn.core.default_sub_cmd import default_sub_cmd

cmd_name = Path(__file__).stem.split('_')[0]


@click.command()
@click.argument('text', required=False, default='')
@click.pass_context
def cli(ctx: click.Context, text) -> None:
    """Create chain of fgn commands."""
    ctx.obj.text = f"""###
The first command must have a -o option to create the output file.
The other commands must have a -i option to read the input file and a -o option to create the output file.
Make sure that the output file is the input file for the next command.
```shell
fgn -o "<TEXT1>.md" COMMAND "<TEXT1>"
fgn -i "<TEXT1>.md" -o "<TEXT2>.md" COMMAND "<TEXT2>"
fgn -i "<TEXT2>.md" -o "<TEXT3>.md" COMMAND "<TEXT3>"
fgn -i "<TEXT3>.md" -o "<TEXT4>.md" COMMAND "<TEXT4>"
```
Provide a ```shell``` code block with the commands to run.
Use fgn to run the commands. For example:
```shell
fgn -o "buisness-plan.md" plan "Business Plan for Selling Ebooks and Classes"
fgn -i "buisness-plan.md" -o "marketing-plan.md" plan "Marketing Plan for Selling Ebooks and Classes"
fgn -i "marketing-plan.md" -o "working-backwards-press-release.md" blog "Amazon Style Working Backwards Press Release for Selling Ebooks and Classes"
fgn -i "working-backwards-press-release.md" -o "customer-success-story.md" nano "Zero to Hero Customer Success Story for Ebooks and Classes"
```

###
{text}
###
These are the chained fgn commands:
```shell
"""
    default_sub_cmd(ctx, cmd_name)

