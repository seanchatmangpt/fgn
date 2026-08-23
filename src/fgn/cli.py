from pathlib import Path

import click

from fgn.core.broker import Broker


@click.command()
@click.argument("message", default="Hello, World", required=False)
@click.option("-o", "--output", type=click.Path(path_type=Path), help="Output file to write the message.")
@click.option("--receipt-dir", type=click.Path(path_type=Path), help="Directory for BRCE receipts.")
def main(message: str, output: Path | None, receipt_dir: Path | None):
    click.echo(message)
    if output:
        Broker(receipt_dir=receipt_dir).write_text(output, message)


if __name__ == "__main__":
    main()
