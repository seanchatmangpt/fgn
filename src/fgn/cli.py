import click


@click.command()
@click.argument("message", default="Hello, World", required=False)
@click.option("-o", "--output", help="Output file to write the message.")
def main(message, output):
    click.echo(message)

    # If the output option is provided, write the message to the file
    if output:
        with open(output, "w") as file:
            file.write(message)


if __name__ == "__main__":
    main()
