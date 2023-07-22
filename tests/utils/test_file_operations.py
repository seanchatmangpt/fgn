import pytest
from pyfakefs.fake_filesystem_unittest import Patcher
from fgn.core.command_context import CommandContext
from fgn.utils.file_operations import (
    load_default_or_context,
    open_file,
    save_relative_to_base,
    open_file_or_raise,
    extract_markdown,
    get_project_root,
    get_norm_path,
)


@pytest.fixture
def fs():
    patcher = Patcher()
    patcher.setUp()
    yield patcher.fs
    patcher.tearDown()


def test_load_default_or_context():
    # Here, you would write tests for the load_default_or_context function.
    # You would need to create a variety of test cases to cover all possibilities.
    pass


def test_open_file(fs):
    fs.create_file("/test.txt", contents="test content")
    assert open_file("/test.txt") == "test content"


def test_save_relative_to_base(fs):
    base_path = "/path/to/base"
    fs.create_dir(base_path)
    save_relative_to_base("test.txt", "test content", base_path)
    with open("/path/to/base/test.txt", "r") as f:
        assert f.read() == "test content"


def test_open_file_or_raise(fs):
    with pytest.raises(FileNotFoundError):
        open_file_or_raise("/nonexistent.txt")
    fs.create_file("/test.txt", contents="test content")
    assert open_file_or_raise("/test.txt") == "test content"


def test_extract_markdown():
    assert (
        extract_markdown("```test\nprint('Hello World!')```") == "print('Hello World!')"
    )
    assert extract_markdown("no markdown here") == "no markdown here"


def test_get_project_root():
    assert str(get_project_root()).endswith("fgn")


def test_get_norm_path_windows(mocker):
    mocker.patch("os.name", "nt")
    assert get_norm_path("/path/to/file") == "\\path\\to\\file"


def test_get_norm_path_non_windows(mocker):
    mocker.patch("os.name", "posix")
    assert get_norm_path("/path/to/file") == "/path/to/file"
