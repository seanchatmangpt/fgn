from pathlib import Path

import click

from fgn.core.broker import Broker, Receipt

cmd_name = Path(__file__).stem.split("_")[0]


def create_command_scaffold(
    new_cmd_name: str,
    *,
    command_root: str | Path,
    broker: Broker | None = None,
) -> list[Receipt]:
    name = new_cmd_name.strip()
    if not name or not name.replace("_", "").isalnum():
        raise ValueError("command name must be alphanumeric with optional underscores")
    new_path = Path(command_root) / name
    if new_path.exists():
        raise FileExistsError(f"{name} already exists")

    writer = broker or Broker()
    config = f"""# fgn/commands/{name}/{name}_config.yml
defaults:
  template: {name}_template.txt
  example: {name}_example.txt
  system_prompt: {name}_system_prompt.txt
  history_path: {name}_history.txt
  model: gpt-4o-mini
  auto_clear: false
  verbose: false
  auto_summarize: 4
"""
    command = f'''# fgn/core/commands/{name}/{name}_cmd.py
from pathlib import Path

import click

from fgn.core.default_sub_cmd import default_sub_cmd

cmd_name = Path(__file__).stem.split("_")[0]


@click.command()
@click.argument("text", required=False, default="")
@click.pass_context
def cli(ctx: click.Context, text: str) -> None:
    """Create {name}."""
    ctx.obj.text = text
    default_sub_cmd(ctx, cmd_name)
'''

    receipts = [
        writer.write_text(new_path / f"{name}_config.yml", config),
        writer.write_text(new_path / f"{name}_cmd.py", command),
    ]
    for filename in (
        f"{name}_example.txt",
        f"{name}_system_prompt.txt",
        f"{name}_history.txt",
        f"{name}_template.txt",
        "__init__.py",
    ):
        receipts.append(writer.write_text(new_path / filename, ""))
    return receipts


@click.command()
@click.argument("text", required=True)
@click.pass_context
def cli(ctx: click.Context, text: str) -> None:
    """Create a receipt-bound FGN command scaffold."""
    ctx.obj.text = text
    try:
        receipts = create_command_scaffold(
            text, command_root=Path(__file__).resolve().parent.parent
        )
    except (ValueError, FileExistsError) as error:
        raise click.ClickException(str(error)) from error
    if any(receipt.status != "ALIVE" for receipt in receipts):
        raise click.ClickException("one or more scaffold writes did not reach ALIVE")
    click.echo(f"created {text.strip()} with {len(receipts)} receipts")
