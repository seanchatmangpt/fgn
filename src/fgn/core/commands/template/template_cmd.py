import os
import io
from pathlib import Path
import click
from rich import print

from fgn.core.default_sub_cmd import default_sub_cmd

cmd_name = Path(__file__).stem.split('_')[0]


@click.command()
@click.argument('text', required=True)
@click.pass_context
def cli(ctx: click.Context, text) -> None:
    """Create a command named by the prompt."""
    ctx.obj.text = text
    new_cmd_name = ctx.obj.text
    path = Path(__file__).parent.absolute()
    new_path = path.parent.absolute() / new_cmd_name

    # Create the  ../{new_cmd_name} folder
    if not new_path.exists():
        new_path.mkdir()
    else:
        print(f"Error: {new_cmd_name} already exists.")
        exit(1)

    # Write to the config file
    with open(new_path / f"{new_cmd_name}_config.yml", "w", encoding="utf-8") as f:
        f.write(f"""# fgn/commands/{new_cmd_name}/{new_cmd_name}_config.yml
defaults:
  template: {new_cmd_name}_template.txt
  example: {new_cmd_name}_example.txt
  system_prompt: {new_cmd_name}_system_prompt.txt
  history_path: {new_cmd_name}_history.txt
  model: gpt-3.5-turbo
  auto_clear: false
  verbose: false
  auto_summarize: int = 4""")

        # Write to the command file
        with open(new_path / f"{new_cmd_name}_cmd.py", "w", encoding="utf-8") as f:
            f.write(f"""# fgn/core/commands/{new_cmd_name}/{new_cmd_name}_cmd.py
from pathlib import Path
import click

from fgn.core.default_sub_cmd import default_sub_cmd

cmd_name = Path(__file__).stem.split('_')[0]


@click.command()
@click.argument('text', required=False, default='')
@click.pass_context
def cli(ctx: click.Context, text) -> None:
    \"\"\"Create {new_cmd_name}.\"\"\"
    ctx.obj.text = text
    default_sub_cmd(ctx, cmd_name)
    """)

        # touch all the new  files
        files = [f"{new_cmd_name}_example.txt", f"{new_cmd_name}_system_prompt.txt", f"{new_cmd_name}_history.txt",
                 f"{new_cmd_name}_template.txt",
                 "__init__.py"]
        for file in files:
            os.system(f"touch {new_path}/{file}")
