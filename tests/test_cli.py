import pytest
from click.testing import CliRunner

from fgn.cli import main


@pytest.fixture
def runner(fs):
    return CliRunner()


def test_file_writer_with_output(runner, fs):
    # Use the fs fixture provided by pytest-fs to create a fake file
    fake_file_path = "/path/to/fake_file.txt"
    fake_file_content = "Test Message"
    message = "Hello World!"
    fs.create_file(fake_file_path, contents=fake_file_content)

    # Use the runner fixture to invoke the CLI command
    result = runner.invoke(main, ["-o", fake_file_path, message])

    # Print the output and contents of the fake file for debugging
    print("result.output:", result.output)
    with open(fake_file_path, "r") as file:
        print("fake_file_content:", file.read())

    # Verify the result
    assert result.exit_code == 0
    assert result.output.strip() == message
