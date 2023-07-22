from pathlib import Path

import click

from fgn.utils.file_operations import create_project_dir


@click.command()
@click.argument("message", default="Hello, World", required=False)
@click.option("-o", "--output", help="Output file to write the message.")
def main(message, output):
    create_project_dir()

    click.echo(message)

    # If the output option is provided, write the message to the file
    if output:
        with open(output, "w") as file:
            file.write(message)


if __name__ == "__main__":
    main()
